from slugify import slugify

create_slug = (lambda text: slugify(text=text))

# def create_slug(text: str) -> str:
#     return slugify(text=text)
