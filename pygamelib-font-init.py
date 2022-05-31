#!/usr/bin/env python3

from pygamelib.gfx import core
from pygamelib import base, constants
import os
import json
import argparse
import string


parser = argparse.ArgumentParser(
    description="A script to easily initialize a new font for the pygamelib. "
    "Please read https://github.com/arnauddupuis/pygamelib/wiki/Font-creation for more "
    "information."
)

parser.add_argument(
    "-s",
    "--scalable",
    action=argparse.BooleanOptionalAction,
    default=False,
    help="Declare the font as scalable. You have to make sure that it is actually "
    "scalable when editing it.",
)

parser.add_argument(
    "-m",
    "--monospace",
    action=argparse.BooleanOptionalAction,
    default=False,
    help="Declare the font as monospace. It means that all characters have the same "
    "width.",
)

parser.add_argument(
    "-c",
    "--colorable",
    action=argparse.BooleanOptionalAction,
    default=True,
    help="Declare the font as colorable. This means that the font is created using 2 "
    "colors (background and foreground) and that the Font class will be able to use"
    " this to allow colorization of the font. Read: "
    "https://github.com/arnauddupuis/pygamelib/wiki/Font-creation for more info.",
)

parser.add_argument(
    "-o",
    "--output-directory",
    type=str,
    action="store",
    required=False,
    default="",
    help="Specify the output directory. If set, all files generated will be store in "
    "that directory. If not, files are going to be stored in the current directory. "
    "The entire directory structure will be created if it does not exist.",
)

parser.add_argument(
    "-d",
    "--default-glyph",
    type=str,
    action="store",
    required=False,
    default="",
    help="Set the default glyph. This glyph will be used when a requested glyph is not"
    " found in the font. If not set, the default glyph will be empty and left for you"
    " to draw. If set, it will be added as a mapping to another existing glyph. "
    "Therefore, the glyph used as default glyph must exist in the font.",
)

parser.add_argument(
    "-w",
    "--width",
    type=int,
    action="store",
    required=False,
    default=8,
    help="Set the width of the glyphs in the font.",
)

parser.add_argument(
    "-he",
    "--height",
    type=int,
    action="store",
    required=False,
    default=4,
    help="Set the width of the glyphs in the font.",
)

parser.add_argument(
    "-hs",
    "--horizontal-spacing",
    type=int,
    action="store",
    required=False,
    default=0,
    help="Specify the horizontal spacing between glyphs.",
)

parser.add_argument(
    "-vs",
    "--vertical-spacing",
    type=int,
    action="store",
    required=False,
    default=0,
    help="Specify the vertical spacing between glyphs.",
)

parser.add_argument(
    "-lc",
    "--lower-case",
    action=argparse.BooleanOptionalAction,
    default=True,
    help="Generate all ASCII lower case glyphs.",
)

parser.add_argument(
    "-uc",
    "--upper-case",
    action=argparse.BooleanOptionalAction,
    default=True,
    help="Generate all ASCII upper case glyphs.",
)

parser.add_argument(
    "-n",
    "--numbers",
    action=argparse.BooleanOptionalAction,
    default=True,
    help="Generate all number glyphs between 0 and 9.",
)

parser.add_argument(
    "-eg",
    "--extra-glyphs",
    action=argparse.BooleanOptionalAction,
    default=True,
    help="Generate extra glyphs like @, #, punctuations, etc.",
)

parser.add_argument(
    "-e",
    "--empty",
    action=argparse.BooleanOptionalAction,
    default=False,
    help="By default, the generated glyph are filled with the character that they "
    "represent. If you prefer to have empty glyphs, use this switch.",
)

parser.add_argument("font_name", help="The name of the font to create.")

args = parser.parse_args()

config = {
    "scalable": args.scalable,
    "monospace": args.monospace,
    "colorable": True,
    "height": args.height,
    "width": args.width,
    "horizontal_spacing": args.horizontal_spacing,
    "vertical_spacing": args.vertical_spacing,
    "fg_color": {"red": 255, "green": 255, "blue": 255},
    "bg_color": None,
    "glyphs_map": {},
}

font_name = args.font_name

output_dir = "."
if args.output_directory:
    output_dir = args.output_directory
font_name = args.font_name

fc = core.SpriteCollection()

white = core.Color(255, 255, 255)

needed_glyphs = [" "] + list(string.ascii_lowercase) + list(string.digits)

if args.lower_case:
    needed_glyphs += list(string.ascii_lowercase)

if args.upper_case:
    needed_glyphs += list(string.ascii_uppercase)

if args.numbers:
    needed_glyphs += list(string.digits)

if args.extra_glyphs:
    needed_glyphs += list(string.punctuation)

if args.default_glyph != "" and args.default_glyph not in needed_glyphs:
    print(
        base.Text(
            f'Glyph "{args.default_glyph}" cannot be the default glyph as it is not in '
            "the list of generated glyphs.",
            fg_color=core.Color(255, 0, 0),
        )
    )
    needed_glyphs = ["default"] + needed_glyphs
    print("The font is generated with the default glyph as empty.")
else:
    config["glyphs_map"]["default"] = args.default_glyph
if args.default_glyph == "":
    needed_glyphs = ["default"] + needed_glyphs

if args.lower_case and not args.upper_case:
    for c in list(string.ascii_lowercase):
        config["glyphs_map"][c.upper()] = c
    print(
        "The mapping from lower case to upper case was automatically added. Now "
        "Font.glyph('a') and Font.glyph('A') will return the same thing."
    )

if args.upper_case and not args.lower_case:
    for c in list(string.ascii_uppercase):
        config["glyphs_map"][c.lower()] = c
    print(
        "The mapping from upper case to lower case was automatically added. Now "
        "Font.glyph('a') and Font.glyph('A') will return the same thing."
    )

print("Generating sprites...", end="")
for char in needed_glyphs:
    spr = None
    model = " "
    if not args.empty:
        if char == "default":
            model = "."
        else:
            model = char
    spr = core.Sprite(
        size=[config["width"], config["height"]],
        default_sprixel=core.Sprixel(" "),
    )
    for row in range(config["height"]):
        for col in range(config["width"]):
            spr.set_sprixel(row, col, core.Sprixel(model, fg_color=white))

    spr.name = char
    fc.add(spr)
print("done")
print("Writting files...", end="")
os.makedirs(f"{output_dir}/pygamelib/assets/fonts/{font_name}", exist_ok=True)
fc.to_json_file(f"{output_dir}/pygamelib/assets/fonts/{font_name}/glyphs.spr")
with open(f"{output_dir}/pygamelib/assets/fonts/{font_name}/config.json", "w") as file:
    json.dump(config, file)

with open(f"{output_dir}/pygamelib/assets/fonts/{font_name}/__init__.py", "w") as file:
    file.write("")

print("done")


print(
    base.Text(
        "Configuration values of the font:",
        core.Color(0, 255, 50),
        style=constants.UNDERLINE,
    )
)
for key in [
    "scalable",
    "monospace",
    "colorable",
    "height",
    "width",
    "horizontal_spacing",
    "vertical_spacing",
    "fg_color",
    "bg_color",
]:
    k = base.Text(f"{key}:", core.Color(0, 255, 255), style=constants.BOLD)
    print(f"{k}: {config[key]}")
print(
    f"{base.Text('Glyphs generated:', core.Color(0, 255, 255), style=constants.BOLD)}: "
    f"{len(needed_glyphs)}"
)
out = base.Text(
    f"{output_dir}/pygamelib/assets/fonts/{font_name}/",
    core.Color(255, 0, 255),
    style=constants.BOLD,
)
print(f"The font was saved in: {out}")
print(
    f"\nThe glyph file ({output_dir}/pygamelib/assets/fonts/{font_name}/glyphs.spr) can"
    " now be edited with pgl-sprite-editor.py."
)
if not args.empty:
    print(
        "\nAll glyphs are filled with the letter that they should represent. If you "
        "want the glyph to be empty, use --empty."
    )
