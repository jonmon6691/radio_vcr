#!/usr/bin/env python3

from PIL import Image, ImageDraw, ImageFont
from font_roboto import Roboto, RobotoMedium, RobotoBold
from inky import InkyPHAT

def getsize(font, text):
    _, _, right, bottom = font.getbbox(text)
    return (right, bottom)

try:
    inky_display = InkyPHAT("yellow")
except TypeError:
    raise TypeError("You need to update the Inky library to >= v1.1.0")

try:
    inky_display.set_border(inky_display.BLACK)
except NotImplementedError:
    pass


def disp_on_air(args):
    print(f"Change display: On now: {args.SHOW}")

    img = Image.open("kmhd_test.png")
    draw = ImageDraw.Draw(img)

    show_x = 31
    show_y = 45

    draw.circle((show_x + 9, show_y + 10), 7, fill=inky_display.YELLOW)

    font = ImageFont.truetype(Roboto, 18)
    time = "Recording..."
    draw.text((show_x + 22, show_y), time, inky_display.WHITE, font)
    time_w, time_h = getsize(font, time)

    font = ImageFont.truetype(RobotoBold, 19)
    show = args.SHOW
    draw.text((show_x, show_y + time_h + 3), show, inky_display.WHITE, font)

    img = img.rotate(180)
    inky_display.set_image(img)
    inky_display.show()

def disp_up_next(args):
    import get_schedule
    next_show = get_schedule.get_next_show_within(7, args.shows)
    if next_show is None:
        print(f"Change display: No show in the next 7 days!")

        img = Image.open("kmhd_test.png")
        draw = ImageDraw.Draw(img)

        show_x = 31
        show_y = 45

        font = ImageFont.truetype(Roboto, 18)
        time = "Next 7 days:"
        draw.text((show_x, show_y), time, inky_display.WHITE, font)
        time_w, time_h = getsize(font, time)

        font = ImageFont.truetype(RobotoBold, 19)
        show = "Nothing scheduled"
        draw.text((show_x, show_y + time_h + 3), show, inky_display.WHITE, font)

        img = img.rotate(180)
        inky_display.set_image(img)
        inky_display.show()
    else:
        time_str = next_show.start.strftime("%I:%M %p %a")
        print(f"Change display: {next_show.title} {time_str}")

        img = Image.open("kmhd_test.png")
        draw = ImageDraw.Draw(img)

        font = ImageFont.truetype(RobotoMedium, 16)
        draw.text((130, 20), "up next:", inky_display.WHITE, font)

        show_x = 31
        show_y = 45

        font = ImageFont.truetype(Roboto, 18)
        time = time_str
        draw.text((show_x, show_y), time, inky_display.WHITE, font)
        time_w, time_h = getsize(font, time)

        font = ImageFont.truetype(RobotoBold, 19)
        show = next_show.title
        draw.text((show_x, show_y + time_h + 3), show, inky_display.WHITE, font)

        img = img.rotate(180)
        inky_display.set_image(img)
        inky_display.show()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help="Subcommand")

    on_air_parser = subparsers.add_parser("on-air", help="Update display to indicate recording in progress")
    on_air_parser.add_argument("SHOW", help="Name of the show that's on now")
    on_air_parser.set_defaults(func=disp_on_air)

    up_next_parser = subparsers.add_parser("up-next", help="Update display after recording is stopped to show next planned recording")
    up_next_parser.add_argument("--shows", help="Show allow-list, one show-name per line")
    up_next_parser.set_defaults(func=disp_up_next)

    args, _ = parser.parse_known_args()
    args.func(args)

exit()
