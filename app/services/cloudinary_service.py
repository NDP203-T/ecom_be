import cloudinary
import cloudinary.uploader
import logging
import re

logger = logging.getLogger(__name__)

class CloudinaryService:
    
    @staticmethod
    def upload_image(file, folder='products'):
        """Upload ảnh lên Cloudinary"""
        try:
            result = cloudinary.uploader.upload(
                file,
                folder=folder,
                resource_type='image'
            )
            return result.get('secure_url')
        except Exception as e:
            logger.error(f"Failed to upload image to Cloudinary: {str(e)}")
            return None
    
    @staticmethod
    def delete_image(public_id):
        """Xóa ảnh trên Cloudinary theo public_id"""
        try:
            result = cloudinary.uploader.destroy(public_id)
            return result.get('result') == 'ok'
        except Exception as e:
            logger.error(f"Failed to delete image from Cloudinary: {str(e)}")
            return False
    
    @staticmethod
    def delete_image_from_url(image_url):
        """Xóa ảnh trên Cloudinary từ URL"""
        try:
            # Extract public_id from URL
            # URL format: https://res.cloudinary.com/{cloud_name}/image/upload/v{version}/{public_id}.{format}
            match = re.search(r'/upload/(?:v\d+/)?(.+)\.\w+$', image_url)
            if match:
                public_id = match.group(1)
                return CloudinaryService.delete_image(public_id)
            return False
        except Exception as e:
            logger.error(f"Failed to extract public_id from URL: {str(e)}")
            return False
