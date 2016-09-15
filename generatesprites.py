from PIL import Image
import os
import re

character_regexp = re.compile(r'layer\-[0-9]+([\w\-]+).png')

character_offset = 0
max_height = 0
images = []

os.mkdir("output")
with open(os.path.join("output", "test.html"), "w") as test_html_file:
    test_html_file.write('<html><head><link href="flair.css" rel="stylesheet"><style>.flair{display:inline-block;}</style></head><body>')
    with open(os.path.join("output", "flair.css"), "w") as outputfile:
        for i, filename in enumerate(os.listdir(os.path.join(os.getcwd(),"inputs"))):
            if filename.startswith("layer"):
                im = Image.open(filename)
                images.append(im)
                r, g, b, a = im.split()
                character = character_regexp.match(filename).groups()[0]

                left, top, right, bottom = a.getbbox()
                width = right - left
                height = bottom - top

                offsetx = 0 - character_offset - left
                offsety = 0 - top

                css = """.flair-{} {{
            background-image: url("sprite.png");
            background-position: {}px {}px;
            width: {}px;
            height: {}px;
        }}
        """.format(character, offsetx, offsety, width, height)

                character_offset += im.width
                max_height = max(max_height, im.height)

                print css
                outputfile.write(css)

                test_html_file.write('<div class="flair flair-{}"></div>'.format(character))

        output_image = Image.new("RGBA", (character_offset, max_height))
        offset = 0
        for im in images:
            output_image.paste(im, (offset, 0))
            offset += im.width
        output_image.save(os.path.join("output", "sprite.png"))

    test_html_file.write("</body>")
