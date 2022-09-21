from minesweeper_solver.game import Game, get_screen
from minesweeper_solver.util import near_same_color


# TODO - Get board that's partially complete
def get_board():
    im = get_screen()
    top_left = None
    box_one_bottom_right = None
    bottom_right = None
    for y in range(im.height):
        if bottom_right:
            break

        if not top_left:
            for x in range(im.width):
                pixel = im.getpixel((x, y))
                if not top_left and near_same_color(pixel, google_colors["light_empty"]):  # Top right of the board
                    top_left = (x, y)
                    break
        elif not box_one_bottom_right:
            pixel = im.getpixel((top_left[0], y))
            if near_same_color(pixel, google_colors["dark_empty"]):  # Next box has started
                for x in range(top_left[0], im.width):  # Skip any x value to the left of the board
                    pixel = im.getpixel((x, y))
                    if near_same_color(pixel, google_colors["light_empty"]):  # Box down and right to top left
                        box_one_bottom_right = (x - 1, y - 1)
                        break
                if box_one_bottom_right is None:
                    return None
        else:
            pixel = im.getpixel((top_left[0], y))
            if not near_same_color(pixel, google_colors["light_empty"]) and not near_same_color(pixel, google_colors[
                "dark_empty"]):
                # Bottom of the board is found, need to find bottom right now
                for x in range(top_left[0], im.width):
                    pixel = im.getpixel((x, y - 1))
                    if not near_same_color(pixel, google_colors["light_empty"]) and not near_same_color(pixel,
                                                                                                        google_colors[
                                                                                                            "dark_empty"]):
                        # Found the left edge on the bottom most pixel
                        bottom_right = (x - 1, y - 1)
                        break
    if not bottom_right:
        return None

    # Make sure to add + 1 because subtracting the 2 gives the distance rather than the total dimensions
    board_dimensions = (bottom_right[0] - top_left[0] + 1, bottom_right[1] - top_left[1] + 1)
    box_dimensions = (box_one_bottom_right[0] - top_left[0] + 1, box_one_bottom_right[1] - top_left[1] + 1)
    return GoogleBoard(top_left, board_dimensions, box_dimensions)


class GoogleBoard(Game):
    def __init__(self, top_left, board_dimensions, box_dimensions):
        super().__init__("Google", top_left, board_dimensions, box_dimensions)

    def tile_value(self, x, y, screen):
        positions = self.tile_range(x, y)
        mid_pixel = screen.getpixel(self.get_mouse_position(x, y))
        tile_area = screen.crop((positions[0][0], positions[1][0], positions[0][1], positions[1][1]))
        unique_colors = tile_area.getcolors(tile_area.size[0] * tile_area.size[1])
        for c in unique_colors:
            color = c[1]
            if near_same_color(color, google_colors["flag"], 10):
                return -1
            elif near_same_color(color, google_colors["one"], 10):
                return 1
            elif near_same_color(color, google_colors["two"], 10):
                return 2
            elif near_same_color(color, google_colors["three"], 10):
                return 3
            elif near_same_color(color, google_colors["four"], 10):
                return 4
            elif near_same_color(color, google_colors["five"], 10):
                return 5
            elif near_same_color(color, google_colors["six"], 10):
                return 6

        if near_same_color(mid_pixel, google_colors["light_open"]) or near_same_color(mid_pixel,
                                                                                      google_colors["dark_open"]):
            return 0
        return None

    # Returns 1 if a loss is detected, returns 2 if a win is detected, returns 0 otherwise
    def game_over(self):
        screen = get_screen()
        for y in range(self.boxes_vertical):
            for x in range(self.boxes_horizontal):
                pos = self.get_mouse_position(x, y)
                pixel = screen.getpixel(pos)
                if near_same_color(pixel, google_colors["results"], 10):
                    return 2
        return 0


google_colors = {
    "light_empty": [(170, 215, 81)],
    "dark_empty": [(162, 209, 73)],
    "light_open": [(224, 195, 163)],
    "dark_open": [(211, 185, 157)],
    "border": [(126, 164, 53)],
    "flag": [(242, 54, 7), (230, 51, 7)],
    "results": [(77, 193, 249)],
    # The colors are gradients, but as long as the color shows on the square it's a number
    "one": [(25, 118, 210), (24, 118, 210), (11, 113, 213)],
    "two": [(55, 141, 59), (78, 148, 72)],
    "three": [(211, 47, 47), (210, 41, 43)],
    "four": [(119, 16, 162), (121, 29, 162)],
    "five": [(255, 139, 0)],
    "six": [(30, 157, 169)]
    # TODO: Add 7 and 8
}
