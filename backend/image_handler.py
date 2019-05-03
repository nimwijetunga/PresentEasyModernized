import models

def create_image_and_add_to_cache(image_url, width, height):
	image = models.Image(**{
				'url': image_url,
				'width': width,
				'height': height
			})
	image.add_image_to_cache()
	return image.uuid
