from libqtile import bar, layout, qtile, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
import subprocess
import os

mod = "mod1"
terminal = guess_terminal()
browser = "firefox"
myTerminal = "alacritty"

# Enable mouse focus following
follow_mouse_focus = True


@hook.subscribe.startup_once
def autostart():
    # TODO: add log msg
    script_path = os.path.expanduser('~/.config/qtile/display.sh')
    subprocess.run(['bash', script_path])
    subprocess.run(['nitrogen', '--restore'])
    subprocess.Popen(['picom', '--backend', 'glx'])

@hook.subscribe.screen_change
def screen_change(event):
    script_path = os.path.expanduser('~/.config/qtile/display.sh')
    subprocess.Popen(['bash', script_path])
    qtile.reconfigure_screens()

keys = [
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(), desc="Toggle split"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod], "f", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen"),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn command prompt"),
    Key([mod], "space", lazy.spawn("/home/abhinav/.config/polybar/hack/scripts/launcher.sh"), desc="Launch application launcher"),
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set +5%")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 5%-")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pamixer --increase 10")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("pamixer --decrease 10")),
    Key([], "XF86AudioMute", lazy.spawn("pamixer --toggle-mute")),
]

groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend([
        Key([mod], i.name, lazy.group[i.name].toscreen(), desc="Switch to group {}".format(i.name)),
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name), desc="Move window to group {}".format(i.name)),
    ])

layouts = [
    layout.MonadTall(
        margin=7,
        border_width=3,
        border_focus="#0000FF",  # Purple border for focused window
        border_normal="#808080",  # Gray border for unfocused windows
        ratio=0.75,
    ),
    layout.Max(),  # Max layout usually doesn't have borders, but you can add if needed
    layout.Columns(
        margin=7,
        border_width=3,
        border_focus="#0000FF",  # Purple border for focused window
        border_normal="#808080",  # Gray border for unfocused windows
    ),
]

widget_defaults = dict(font="sans", fontsize=12, padding=3)
extension_defaults = widget_defaults.copy()


primary_bar = bar.Bar(
    [
        widget.GroupBox(),
        widget.CurrentLayoutIcon(),
        widget.Spacer(length=bar.STRETCH),
        widget.Clock(format='%a %I:%M %p'),
        widget.Spacer(length=bar.STRETCH),
        widget.Memory(
            format=' {MemPercent}%',  # Display memory used, total, and percentage
            update_interval=3.0,  # Update interval in seconds
        ),
        widget.CPU(
            format='{load_percent}%'
        ),
    ],
    28,  # Bar size (height in pixels)
    background="#00000080"  # Transparent background for the bar
)

secondary_bar = bar.Bar(
    [
        widget.GroupBox(),
        widget.CurrentLayoutIcon(),
        widget.Spacer(length=bar.STRETCH),
        widget.Clock(format='%a %I:%M %p'),
        widget.Spacer(length=bar.STRETCH),
        widget.Systray(),
        widget.Memory(),
    ],
    28,  # Bar size (height in pixels)
    background="#00000080"  # Transparent background for the bar
)

screens = [
    Screen(top=primary_bar),
    Screen(top=secondary_bar),
]

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

floating_layout = layout.Floating(float_rules=[*layout.Floating.default_float_rules, Match(wm_class="confirmreset"), Match(wm_class="makebranch"), Match(wm_class="maketag"), Match(wm_class="ssh-askpass"), Match(title="branchdialog"), Match(title="pinentry"),])
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = True
wl_input_rules = None
wl_xcursor_theme = None
wl_xcursor_size = 24
wmname = "LG3D"
