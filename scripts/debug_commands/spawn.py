from typing import List

from scripts.cat.enums import CatAge
from scripts.cat.factories.new_cat_factory import NewCatFactory
from scripts.cat.pelts import Pelt
from scripts.cat.sprites.load_sprites import Sprites, sprites
from scripts.debug_commands.command import Command
from scripts.debug_commands.utils import add_output_line_to_log
from scripts.game_structure import game, constants


class SpawnPeltsCommand(Command):
    name = "pelts"
    description = "Spawn a cat of each colour for a given pelt."
    usage = "<species: str|folder: int> <pelt_name: str>"
    alias = ["pelt", "p"]

    def callback(self, args: List[str]):
        species_list = list(constants.SPECIES["species"].keys())
        if len(args) < 1:
            add_output_line_to_log(
                f"Must specify a species or sprite folder! Possible species are {species_list}."
            )
            return
        folder = args[0]
        if not folder.isdigit():
            if folder not in species_list:
                add_output_line_to_log(
                    f"Species {folder} does not seem to exist! Possible species are {species_list}."
                )
                return
            else:
                folder = species_list.index(folder) + 1
        folder = int(folder)

        possible_pelts_str = ", ".join(
            set(getattr(Sprites, f"PELT_TO_RECIPE_{folder}").keys()) - {"Tortie", "Calico"}
        )
        if len(args) < 2:
            add_output_line_to_log(
                f"Must specify a pelt! Possible pelts are {possible_pelts_str}."
            )
            return

        pelt_name = args[1]
        if pelt_name not in getattr(Sprites, f"PELT_TO_RECIPE_{folder}").keys():
            add_output_line_to_log(
                f"Pelt {pelt_name} does not seem to exist! Possible pelts are {possible_pelts_str}."
            )
            return

        for colour in getattr(Sprites, f"PELT_COLOR_PALETTES_{folder}"):
            cat = NewCatFactory.create_cat(
                prefix=f"{colour}_{pelt_name}",
                suffix="",
                species=species_list[folder-1],
                moons=60,
                pelt=Pelt(
                    name=pelt_name,
                    colour=colour,
                ),
            )
            cat.pelt.cat_sprites["adult"] = "adult_short2"
            game.clan.add_cat(cat)
            add_output_line_to_log(f"Added {cat.name} with ID {cat.ID}")


class SpawnColoursCommand(Command):
    name = "colours"
    description = "Spawn a cat of each pelt for a given colour."
    usage = "<species: str|folder: int> <colour: str>"
    aliases = ["color", "colors", "colour", "c"]

    def callback(self, args: List[str]):
        species_list = list(constants.SPECIES["species"].keys())
        if len(args) < 1:
            add_output_line_to_log(
                f"Must specify a species or sprite folder! Possible species are {species_list}."
            )
            return
        folder = args[0]
        if not folder.isdigit():
            if args[0] not in species_list:
                add_output_line_to_log(
                    f"Species {folder} does not seem to exist! Possible species are {species_list}."
                )
                return
            else:
                folder = species_list.index(folder) + 1
        folder = int(folder)

        possible_colours_str = ", ".join(getattr(Sprites, f"PELT_COLOR_PALETTES_{folder}").keys())

        if len(args) < 2:
            add_output_line_to_log(
                f"Must specify a colour! Possible colours are {possible_colours_str}."
            )
            return

        colour = args[1]
        if colour not in getattr(Sprites, f"PELT_COLOR_PALETTES_{folder}"):
            add_output_line_to_log(
                f"Colour {colour} does not seem to exist! This command is case sensitive. Possible colours are {possible_colours_str}."
            )
            return

        for pelt_name in getattr(Sprites, f"PELT_TO_RECIPE_{folder}"):
            if pelt_name in ("Tortie", "Calico"):
                continue
            cat = NewCatFactory.create_cat(
                prefix=f"{pelt_name}_{colour}",
                suffix="",
                species=species_list[folder-1],
                moons=60,
                pelt=Pelt(
                    name=pelt_name,
                    colour=colour,
                ),
            )
            cat.pelt.cat_sprites["adult"] = "adult_short2"
            game.clan.add_cat(cat)
            add_output_line_to_log(f"Added {cat.name} with ID {cat.ID}")


class SpawnTintColoursCommand(Command):
    name = "tint_colours"
    description = "Spawn a cat of each colour for a given pelt and tint."
    usage = "<species: str|folder: int> <pelt_name: str> <tint: str>"
    aliases = ["tc", "t_c", "tint_colors", "tint_colour", "tint_color"]

    def callback(self, args: List[str]):
        species_list = list(constants.SPECIES["species"].keys())
        if len(args) < 1:
            add_output_line_to_log(
                f"Must specify a species or sprite folder! Possible species are {species_list}."
            )
            return
        folder = args[0]
        if not folder.isdigit():
            if args[0] not in species_list:
                add_output_line_to_log(
                    f"Species {folder} does not seem to exist! Possible species are {species_list}."
                )
                return
            else:
                folder = species_list.index(folder) + 1
        folder = int(folder)

        possible_pelts_str = ", ".join(
            set(getattr(Sprites, f"PELT_TO_RECIPE_{folder}").keys()) - {"Tortie", "Calico"}
        )
        if len(args) < 3:
            add_output_line_to_log(f"Must specify a pelt and tint! (in that order)")
            return

        pelt_name = args[1]
        if pelt_name not in getattr(Sprites, f"PELT_TO_RECIPE_{folder}"):
            add_output_line_to_log(
                f"Pelt {pelt_name} does not seem to exist! Possible pelts are {possible_pelts_str}."
            )
            return

        tint_colours = list(getattr(sprites, f"cat_tints_{folder}")["tint_colours"].keys())
        dilute_tint_colours = list(getattr(sprites, f"cat_tints_{folder}")["dilute_tint_colours"].keys())
        remove_tone_tint_colours = list(getattr(sprites, f"cat_tints_{folder}")["remove_tone_tint_colours"].keys())

        possible_tints_str = ", ".join(
            set(tint_colours and dilute_tint_colours and remove_tone_tint_colours)
        )

        tint_name = args[2]
        if not (
            tint_name in tint_colours + dilute_tint_colours + remove_tone_tint_colours
        ):
            add_output_line_to_log(
                f"Tint {tint_name} does not seem to exist! Possible tints are {possible_tints_str}."
            )
            return

        for colour in getattr(Sprites, f"PELT_COLOR_PALETTES_{folder}"):
            cat = NewCatFactory.create_cat(
                prefix=f"{tint_name}_{pelt_name}_{colour}",
                suffix="",
                species=species_list[folder-1],
                moons=60,
                pelt=Pelt(name=pelt_name, colour=colour, tint=tint_name),
            )
            cat.pelt.cat_sprites["adult"] = "adult_short2"
            game.clan.add_cat(cat)
            add_output_line_to_log(f"Added {cat.name} with ID {cat.ID}")


class SpawnTintsCommand(Command):
    name = "tints"
    description = "Spawn a cat of each tint for a given pelt and colour."
    usage = "<species: str|folder: int> <pelt_name: str> <colour: str>"
    aliases = ["tint", "t"]

    def callback(self, args: List[str]):
        species_list = list(constants.SPECIES["species"].keys())
        if len(args) < 1:
            add_output_line_to_log(
                f"Must specify a species or sprite folder! Possible species are {species_list}."
            )
            return
        folder = args[0]
        if not folder.isdigit():
            if args[0] not in species_list:
                add_output_line_to_log(
                    f"Species {folder} does not seem to exist! Possible species are {species_list}."
                )
                return
            else:
                folder = species_list.index(folder) + 1
        folder = int(folder)

        if len(args) < 3:
            add_output_line_to_log(f"Must specify a pelt and colour! (in that order)")
            return

        pelt = args[1]
        possible_pelts_str = ", ".join(
            set(getattr(Sprites, f"PELT_TO_RECIPE_{folder}").keys()) - {"Tortie", "Calico"}
        )
        if pelt not in getattr(Sprites, f"PELT_TO_RECIPE_{folder}"):
            add_output_line_to_log(
                f"Pelt {pelt} does not seem to exist! Possible pelts are {possible_pelts_str}."
            )
            return

        if pelt in ("Tortie", "Calico"):
            add_output_line_to_log(f"Pelt cannot be Tortie or Calico!")
            return

        colour = args[2]
        possible_colours_str = ", ".join(getattr(Sprites, f"PELT_COLOR_PALETTES_{folder}").keys())
        if colour not in getattr(Sprites, f"PELT_COLOR_PALETTES_{folder}"):
            add_output_line_to_log(
                f"Colour {colour} does not seem to exist! Possible colours are {possible_colours_str}."
            )
            return

        base_tints = getattr(sprites, f"cat_tints_{folder}")["possible_tints"]["basic"]
        if colour in getattr(sprites, f"cat_tints_{folder}")["colour_groups"]:
            color_group = getattr(sprites, f"cat_tints_{folder}")["colour_groups"].get(colour, "warm")
            colour_tints = getattr(sprites, f"cat_tints_{folder}")["possible_tints"][color_group]
        else:
            colour_tints = []
        possible_tints = [None] + base_tints + colour_tints

        for tint in possible_tints:
            cat = NewCatFactory.create_cat(
                prefix=f"{tint}_{pelt}_{colour}",
                suffix="",
                species=species_list[folder-1],
                moons=60,
                pelt=Pelt(name=pelt, colour=colour, tint=tint),
            )
            cat.pelt.cat_sprites["adult"] = "adult_short2"
            game.clan.add_cat(cat)
            add_output_line_to_log(f"Added {cat.name} with ID {cat.ID}")


class SpawnCommand(Command):
    name = "spawn"
    description = "Spawn specific sets of cats to test things"
    aliases = ["sp"]

    sub_commands = [
        SpawnPeltsCommand(),
        SpawnColoursCommand(),
        SpawnTintsCommand(),
        SpawnTintColoursCommand(),
    ]

    def callback(self, args: List[str]):
        add_output_line_to_log("Please specify a subcommand")
