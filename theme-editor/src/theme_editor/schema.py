from __future__ import annotations

HOVERED_DESCRIPTION = "Same as above, in hovered state."
PRESSED_DESCRIPTION = "Same as above, in pressed state."
DISABLED_DESCRIPTION = "Same as above, in disabled state."

ALPHA_COLOR_FIELDS = {
    "focusColor",
    "semiTransparentColor1",
    "semiTransparentColor2",
    "semiTransparentColor3",
    "semiTransparentColor4",
    "shadowColor1",
    "shadowColor2",
    "shadowColor3",
    "statusColorForegroundDisabled",
}

COLOR_SECTIONS: tuple[dict[str, object], ...] = (
    {
        "title": "Primary Color",
        "rows": (
            ("subtitle", "Background"),
            ("description", "Used to highlight elements."),
            (
                "color",
                "primaryColor",
                "Highlighted elements (default, checked or selected).",
            ),
            ("color", "primaryColorHovered", HOVERED_DESCRIPTION),
            ("color", "primaryColorPressed", PRESSED_DESCRIPTION),
            ("color", "primaryColorDisabled", DISABLED_DESCRIPTION),
            ("subtitle", "Foreground"),
            ("description", "Text drawn over highlighted elements."),
            (
                "color",
                "primaryColorForeground",
                "Text written over highlighted elements.",
            ),
            ("color", "primaryColorForegroundHovered", HOVERED_DESCRIPTION),
            ("color", "primaryColorForegroundPressed", PRESSED_DESCRIPTION),
            ("color", "primaryColorForegroundDisabled", DISABLED_DESCRIPTION),
            ("subtitle", "Alternative"),
            (
                "description",
                "Used to highlight elements over already highlighted elements.",
            ),
            (
                "color",
                "primaryAlternativeColor",
                "A darker/lighter tint for highlighted elements over already highlighted elements.",
            ),
            ("color", "primaryAlternativeColorHovered", HOVERED_DESCRIPTION),
            ("color", "primaryAlternativeColorPressed", PRESSED_DESCRIPTION),
            ("color", "primaryAlternativeColorDisabled", DISABLED_DESCRIPTION),
        ),
    },
    {
        "title": "Secondary Color",
        "rows": (
            ("subtitle", "Background"),
            (
                "description",
                "A more neutral color, used for text and non-highlighted elements.",
            ),
            ("color", "secondaryColor", "Text."),
            ("color", "secondaryColorHovered", HOVERED_DESCRIPTION),
            ("color", "secondaryColorPressed", PRESSED_DESCRIPTION),
            ("color", "secondaryColorDisabled", DISABLED_DESCRIPTION),
            ("subtitle", "Foreground"),
            ("description", "Text drawn over elements in secondary color."),
            (
                "color",
                "secondaryColorForeground",
                "Text written over elements that already have text color.",
            ),
            ("color", "secondaryColorForegroundHovered", HOVERED_DESCRIPTION),
            ("color", "secondaryColorForegroundPressed", PRESSED_DESCRIPTION),
            ("color", "secondaryColorForegroundDisabled", DISABLED_DESCRIPTION),
        ),
    },
    {
        "title": "Secondary Alternative Color",
        "rows": (
            ("description", "A lighter version of the secondary color."),
            ("color", "secondaryAlternativeColor", "Less important text."),
            ("color", "secondaryAlternativeColorHovered", HOVERED_DESCRIPTION),
            ("color", "secondaryAlternativeColorPressed", PRESSED_DESCRIPTION),
            ("color", "secondaryAlternativeColorDisabled", DISABLED_DESCRIPTION),
        ),
    },
    {
        "title": "Neutral Color",
        "rows": (
            ("description", "Used for neutral surfaces and controls."),
            ("color", "neutralColor", "Neutral interactive elements, such as buttons."),
            ("color", "neutralColorHovered", HOVERED_DESCRIPTION),
            ("color", "neutralColorPressed", PRESSED_DESCRIPTION),
            ("color", "neutralColorDisabled", DISABLED_DESCRIPTION),
        ),
    },
    {
        "title": "Semi-transparent Color",
        "rows": (
            ("description", "Used for semi-transparent elements such as scrollbars."),
            (
                "color",
                "semiTransparentColor1",
                "To be used over another color to lighten/darken it.",
            ),
            ("color", "semiTransparentColor2", "Same as above but more contrast."),
            ("color", "semiTransparentColor3", "Same as above but more contrast."),
            ("color", "semiTransparentColor4", "Same as above but more contrast."),
        ),
    },
    {
        "title": "Background Color",
        "rows": (
            (
                "description",
                "Used for containers: windows, group boxes, and other surfaces.",
            ),
            (
                "color",
                "backgroundColorMain1",
                "Textfields, checkboxes, radiobuttons background.",
            ),
            ("color", "backgroundColorMain2", "Window background."),
            ("color", "backgroundColorMain3", "Container background, more contrast."),
            ("color", "backgroundColorMain4", "Same as above, more contrast."),
            ("color", "backgroundColorWorkspace", "Window workspace background."),
            ("color", "backgroundColorTabBar", "QTabBar background."),
        ),
    },
    {
        "title": "Border Color",
        "rows": (
            (
                "description",
                "Used to draw borders for combo boxes, group boxes, and other controls.",
            ),
            (
                "color",
                "borderColor",
                "Borders of textfields, checkboxes, radiobuttons, switches and other elements.",
            ),
            ("color", "borderColorHovered", HOVERED_DESCRIPTION),
            ("color", "borderColorPressed", PRESSED_DESCRIPTION),
            ("color", "borderColorDisabled", DISABLED_DESCRIPTION),
        ),
    },
    {
        "title": "Focus Color",
        "rows": (
            (
                "color",
                "focusColor",
                "Border around the widget that has keyboard focus with QFocusFrame.",
            ),
        ),
    },
    {
        "title": "Shadow Color",
        "rows": (
            ("color", "shadowColor1", "Shadow for elevated elements."),
            ("color", "shadowColor2", "Same as above, more contrast."),
            ("color", "shadowColor3", "Same as above, more contrast."),
        ),
    },
    {
        "title": "Status Color",
        "rows": (
            (
                "description",
                "Displaying feedback to the user such as errors, warnings, and success states.",
            ),
            ("subtitle", "Error"),
            ("color", "statusColorError", "Feedback for error."),
            ("color", "statusColorErrorHovered", HOVERED_DESCRIPTION),
            ("color", "statusColorErrorPressed", PRESSED_DESCRIPTION),
            ("color", "statusColorErrorDisabled", DISABLED_DESCRIPTION),
            ("subtitle", "Warning"),
            ("color", "statusColorWarning", "Feedback for warning."),
            ("color", "statusColorWarningHovered", HOVERED_DESCRIPTION),
            ("color", "statusColorWarningPressed", PRESSED_DESCRIPTION),
            ("color", "statusColorWarningDisabled", DISABLED_DESCRIPTION),
            ("subtitle", "Success"),
            ("color", "statusColorSuccess", "Feedback for success/validity."),
            ("color", "statusColorSuccessHovered", HOVERED_DESCRIPTION),
            ("color", "statusColorSuccessPressed", PRESSED_DESCRIPTION),
            ("color", "statusColorSuccessDisabled", DISABLED_DESCRIPTION),
            ("subtitle", "Info"),
            ("color", "statusColorInfo", "Feedback for information."),
            ("color", "statusColorInfoHovered", HOVERED_DESCRIPTION),
            ("color", "statusColorInfoPressed", PRESSED_DESCRIPTION),
            ("color", "statusColorInfoDisabled", DISABLED_DESCRIPTION),
            ("subtitle", "Foreground"),
            ("description", "Used to draw text over status colors."),
            ("color", "statusColorForeground", "Text over status colors."),
            ("color", "statusColorForegroundHovered", HOVERED_DESCRIPTION),
            ("color", "statusColorForegroundPressed", PRESSED_DESCRIPTION),
            ("color", "statusColorForegroundDisabled", DISABLED_DESCRIPTION),
        ),
    },
)

METADATA_FIELDS: tuple[tuple[str, str], ...] = (
    ("name", "Name of the Qlementine theme"),
    ("author", "Author of the Qlementine theme"),
    ("version", "Version of the Qlementine theme"),
)
