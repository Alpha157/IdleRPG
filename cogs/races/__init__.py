"""
The IdleRPG Discord Bot
Copyright (C) 2018-2019 Diniboy and Gelbpunkt
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.
You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import discord

from discord.ext import commands

from utils.checks import has_char, is_nothing


class Races(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @has_char()
    @is_nothing()
    @commands.command()
    @locale_doc
    async def race(self, ctx):
        _("""Change your race. This is irreversible.""")
        embeds = [
            discord.Embed(
                title=_("Human"),
                description=_(
                    "Humans are a team. They work and fight hand in hand and never give up, even when some of their friends already died. Their rage and hate against enemies makes them attack efficient and concentrated. Their attack and defense skills are pretty equal."
                ),
                color=self.bot.config.primary_colour,
            ),
            discord.Embed(
                title=_("Dwarf"),
                description=_(
                    "Dwarves are the masters of their forge. Although they're very small, they can deal a lot of damage with their self-crafted equipment. Because of their reflexes, they have more defense than attack. Want an ale?"
                ),
                color=self.bot.config.primary_colour,
            ),
            discord.Embed(
                title=_("Elf"),
                description=_(
                    "Elves are the masteres of camouflage. They melt with their enviroment to attack enemies without their knowing. Their bound to nature made them good friends of the wild spirits which they can call for help and protection. They have more attack than defense."
                ),
                color=self.bot.config.primary_colour,
            ),
            discord.Embed(
                title=_("Orc"),
                description=_(
                    "Orcs are a friendly race based on their rituals of calling their ancestors to bless the rain and the deeds of their tribe. More ugly than nice, they mostly avoid being attacked by enemies. If they can't avoid a fight, then they have mostly no real damage, only a bit, but a huge armour. Who cares about the damage as long as you don't die?"
                ),
                color=self.bot.config.primary_colour,
            ),
            discord.Embed(
                title=_("Jikill"),
                description=_(
                    "Jikills are dwarflike creatures with one eye in the middle of their face, which lets them have a big and huge forehead, big enough for their brain which can kill enemies. These sensitive creatures are easily knocked out."
                ),
                color=self.bot.config.primary_colour,
            ),
        ]
        races = ["Human", "Dwarf", "Elf", "Orc", "Jikill"]
        questions = {
            "Human": {
                "question": _("One of my biggest regrets is..."),
                "answers": [
                    _("...that I never confessed my true love, and now she is dead."),
                    _("...that I have never been to the funeral of my parents."),
                    _("...that I betrayed my best friend."),
                ],
            },
            "Dwarf": {
                "question": _("One of my proudest creations is..."),
                "answers": [
                    _("...a perfected ale keg."),
                    _("...a magical infused glove."),
                    _("...a bone-forged axe."),
                ],
            },
            "Elf": {
                "question": _("My favourite spirit of the wild is..."),
                "answers": [
                    _("...Beringor, the bear spirit."),
                    _("...Neysa, the tiger spirit."),
                    _("...Avril, the wolf spirit."),
                    _("...Sambuca, the eagle spirit."),
                ],
            },
            "Orc": {
                "question": _("The ancestor that gives me my strength is..."),
                "answers": [
                    _("...my sister."),
                    _("...my father."),
                    _("...my grandmother."),
                    _("...my uncle."),
                ],
            },
            "Jikill": {
                "question": _("The biggest action that can outknock me, is..."),
                "answers": [
                    _("...noise"),
                    _("...spiritual pain"),
                    _("...extreme temperatures."),
                    _("...strange and powerful smells."),
                ],
            },
        }
        race_ = await self.bot.paginator.ChoosePaginator(
            extras=embeds, choices=races
        ).paginate(ctx)
        cv = questions[race_]
        answer = await self.bot.paginator.Choose(
            title=cv["question"], entries=cv["answers"], return_index=True
        ).paginate(ctx)
        await self.bot.pool.execute(
            'UPDATE profile SET "race"=$1, "cv"=$2 WHERE "user"=$3;',
            race_,
            answer,
            ctx.author.id,
        )
        await ctx.send(_("You are now a {race}.").format(race=race_))


def setup(bot):
    bot.add_cog(Races(bot))
