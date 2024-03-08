import pygame, pygame_gui

class HealthBar(pygame_gui.elements.UIProgressBar):
    def __init__(self, rect, manager, player):
        super().__init__(relative_rect=rect, manager=manager)
        self.player = player

    def update(self, time_delta: float):
        self.maximum_progress = max(1.0, self.player.character.max_health)
        self.current_progress = self.player.character.health
        self.percent_full = 100 * self.current_progress / self.maximum_progress

        return super().update(time_delta)
    
class ManaBar(pygame_gui.elements.UIProgressBar):
    def __init__(self, rect, manager, player):
        super().__init__(relative_rect=rect, manager=manager)
        self.player = player

    def update(self, time_delta: float):
        self.maximum_progress = max(1.0, self.player.character.max_mana)
        self.current_progress = self.player.character.mana
        self.percent_full = 100 * self.current_progress / self.maximum_progress

        return super().update(time_delta)
    
class FPSCounter(pygame_gui.elements.UILabel):
    def __init__(self, rect, manager):
        super().__init__(relative_rect=rect, manager=manager, text="Debug")
        self.times = []
        
    def compute_average(self):
        average = 0.0
        for val in self.times:
            average += val
        return 1 / (average / len(self.times))


    def update(self, time_delta: float):
        self.times.append(time_delta)
        if (len(self.times) > 10):
            self.times.remove(self.times[0])

        self.set_text("FPS: " + str(self.compute_average()))

        return super().update(time_delta)
    
class MessageBox(pygame_gui.elements.UITextBox):
    def __init__(self, rect, manager, loop):
        super().__init__(relative_rect=rect, manager=manager, html_text="Error")
        self.loop = loop #Store loop to retrieve messages

    def update(self, time_delta: float):
        
        self.set_text(html_text="".join([message + "<br>" for message in (self.loop.messages)]))

        return super().update(time_delta)
    
class LevelUpHeader(pygame_gui.elements.UILabel):
    def __init__(self, rect, manager, player):
        super().__init__(relative_rect=rect, manager=manager, text="Allocate " + str(player.stat_points) + " Stat Points")
        self.player = player

    def update(self, time_delta: float):
        self.set_text("Allocate " + str(self.player.stat_points - sum(self.player.stat_decisions)) + " Stat Points")
        return super().update(time_delta)
    
class StatChangeText(pygame_gui.elements.UILabel):
    def __init__(self, rect, manager, player, index):
        super().__init__(relative_rect=rect, manager=manager, text="+" + str(player.stat_decisions[index]))
        self.player = player
        self.index = index

    def update(self, time_delta: float):
        self.set_text("+" + str(self.player.stat_decisions[self.index]))

        return super().update(time_delta)
    
    
class StatBox(pygame_gui.elements.UITextBox):
    def __init__(self, rect, manager, player):
        super().__init__(relative_rect=rect, manager=manager, html_text="Error")
        self.player = player

    #HORRIBLE HACK - THIS IS ALSO DEFINED IN DISPLAY.PY - KEEP THEM SYNCED!
    def get_status_text(self, entity):
        status = "Healthy"
        if entity.character.health < entity.character.max_health // 3 * 2:
            status = "Wounded"
        effects = entity.character.status_effects
        for effect in effects:
            status += ", " + effect.description()
        return status
    
    def get_level_text(self, entity):
        if entity.stat_points > 0:
            return "<shadow size=1 offset=0,0 color=#306090><font color=#E0F0FF>Level: " \
                    + str(entity.level) + " (Press L to allocate stat points)</font></shadow>"
        else:
            to_next_level = str(format(entity.experience / entity.experience_to_next_level, ".1%"))
            return "Level: " + str(entity.level) + " (" + to_next_level + " there to next level)"

    def update(self, time_delta: float):
        self.set_text(html_text="Player:<br>" +
                        "Strength: " + str(self.player.character.strength) + "<br>"
                        "Dexterity: " + str(self.player.character.dexterity) + "<br>"
                        "Endurance: " + str(self.player.character.endurance) + "<br>"
                        "Intelligence: " + str(self.player.character.intelligence) + "<br>"
                        "<br>"
                        "Status: " + self.get_status_text(self.player) + "<br>" + \
                        self.get_level_text(self.player) + "<br>")

        return super().update(time_delta)
    
class DepthDisplay(pygame_gui.elements.UILabel):
    def __init__(self, rect, manager, loop):
        super().__init__(relative_rect=rect, manager=manager, text="Error")
        self.loop = loop

    def update(self, time_delta: float):
        self.set_text("Depth " + str(self.loop.generator.depth))

        return super().update(time_delta)