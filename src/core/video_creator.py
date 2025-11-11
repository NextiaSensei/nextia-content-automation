import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os
from config.settings import VIDEO_OUTPUT

class DualScreenVideoCreator:
    """Crea videos con doble pantalla (lado a lado)"""
    
    def __init__(self, output_dir=VIDEO_OUTPUT):
        self.output_dir = output_dir
    
    def create_dual_screen_video(self, script, output_filename, fps=30):
        """
        Crea video con dos pantallas:
        - Izquierda: Visual (puede ser imagen estática, loop, etc)
        - Derecha: Voiceover text animado
        """
        
        # Dimensiones
        height = 1080
        left_width = height  # Cuadrado
        right_width = height
        total_width = left_width + right_width
        
        # Crear video
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(
            os.path.join(self.output_dir, output_filename),
            fourcc,
            fps,
            (total_width, height)
        )
        
        duration = script.get("duration", 60)
        total_frames = duration * fps
        
        for frame_idx in range(total_frames):
            # Encuentra la scene actual basado en timestamp
            current_time = frame_idx / fps
            current_scene = self._get_current_scene(script["scenes"], current_time)
            
            if not current_scene:
                continue
            
            # Crea el frame
            frame = np.zeros((height, total_width, 3), dtype=np.uint8)
            
            # LADO IZQUIERDO: Visual (color sólido o imagen)
            left_visual = np.ones((height, left_width, 3), dtype=np.uint8) * 30
            cv2.putText(
                left_visual,
                current_scene.get("left_visual", "")[:30],
                (50, height // 2),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.5,
                (255, 255, 255),
                2
            )
            
            # LADO DERECHO: Voiceover text
            right_text = np.ones((height, right_width, 3), dtype=np.uint8) * 60
            text_to_show = current_scene.get("right_voiceover", "")
            
            # Wordwrap
            words = text_to_show.split()
            y_offset = 100
            for i, word in enumerate(words):
                if (i + 1) % 5 == 0:
                    cv2.putText(
                        right_text,
                        word,
                        (50, y_offset),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.2,
                        (255, 200, 0),
                        2
                    )
                    y_offset += 80
                else:
                    cv2.putText(
                        right_text,
                        word,
                        (50, y_offset),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.2,
                        (200, 200, 200),
                        2
                    )
            
            # Combina ambos lados
            frame[:, :left_width] = left_visual
            frame[:, left_width:] = right_text
            
            out.write(frame)
        
        out.release()
        print(f"✅ Video creado: {output_filename}")
    
    def _get_current_scene(self, scenes, current_time):
        """Obtiene la scene actual según el timestamp"""
        for scene in scenes:
            ts = scene.get("timestamp", "00:00-00:00")
            start, end = ts.split("-")
            start_sec = self._timestamp_to_seconds(start)
            end_sec = self._timestamp_to_seconds(end)
            
            if start_sec <= current_time <= end_sec:
                return scene
        return scenes[0] if scenes else None
    
    @staticmethod
    def _timestamp_to_seconds(ts_str):
        """Convierte MM:SS a segundos"""
        parts = ts_str.split(":")
        return int(parts[0]) * 60 + int(parts[1])
