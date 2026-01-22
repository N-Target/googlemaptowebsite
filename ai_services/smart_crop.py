"""
Smart Crop AI - Automatic image cropping and optimization
"""

from PIL import Image, ImageOps
import os

class SmartCropAI:
    def __init__(self):
        self.target_sizes = {
            'hero': (1920, 1080),
            'thumbnail': (400, 300),
            'profile': (300, 300),
            'gallery': (800, 600)
        }
    
    def crop_smart(self, image_path, output_path, crop_type='hero'):
        """
        Intelligently crop image to target size
        """
        try:
            img = Image.open(image_path)
            target_size = self.target_sizes.get(crop_type, self.target_sizes['hero'])
            
            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Calculate aspect ratios
            img_ratio = img.width / img.height
            target_ratio = target_size[0] / target_size[1]
            
            if img_ratio > target_ratio:
                # Image is wider - crop width
                new_width = int(img.height * target_ratio)
                left = (img.width - new_width) // 2
                img = img.crop((left, 0, left + new_width, img.height))
            else:
                # Image is taller - crop height
                new_height = int(img.width / target_ratio)
                top = (img.height - new_height) // 2
                img = img.crop((0, top, img.width, top + new_height))
            
            # Resize to target size
            img = img.resize(target_size, Image.Resampling.LANCZOS)
            
            # Optimize and save
            img.save(output_path, 'JPEG', quality=85, optimize=True)
            
            return output_path
        except Exception as e:
            print(f"Error in smart crop: {e}")
            return None
    
    def optimize_for_web(self, image_path, output_path, max_size_kb=200):
        """
        Optimize image for web delivery
        """
        try:
            img = Image.open(image_path)
            
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Start with high quality
            quality = 95
            
            # Reduce quality until file size is acceptable
            while quality > 20:
                img.save(output_path, 'JPEG', quality=quality, optimize=True)
                
                file_size_kb = os.path.getsize(output_path) / 1024
                if file_size_kb <= max_size_kb:
                    break
                
                quality -= 5
            
            return output_path
        except Exception as e:
            print(f"Error in optimization: {e}")
            return None
    
    def create_responsive_set(self, image_path, output_dir):
        """
        Create responsive image set
        """
        sizes = {
            'small': 480,
            'medium': 768,
            'large': 1200,
            'xlarge': 1920
        }
        
        output_paths = {}
        
        try:
            img = Image.open(image_path)
            
            for size_name, width in sizes.items():
                # Calculate proportional height
                ratio = width / img.width
                height = int(img.height * ratio)
                
                # Resize
                resized = img.resize((width, height), Image.Resampling.LANCZOS)
                
                # Save
                output_path = os.path.join(output_dir, f"{size_name}.jpg")
                resized.save(output_path, 'JPEG', quality=85, optimize=True)
                
                output_paths[size_name] = output_path
            
            return output_paths
        except Exception as e:
            print(f"Error creating responsive set: {e}")
            return None

if __name__ == "__main__":
    # Test
    smart_crop = SmartCropAI()
    print("Smart Crop AI initialized")
