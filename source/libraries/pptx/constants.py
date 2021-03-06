# -*- coding: utf-8 -*-
#
# constants.py
#
# Copyright (C) 2012, 2013 Steve Canny scanny@cisco.com
#
# This module is part of python-pptx and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

"""
Constant values modeled after those in the MS Office API.
"""


class MSO(object):
    """
    Constants corresponding to things like ``msoAnchorMiddle`` in the MS
    Office API.
    """
    # _TextFrame.vertical_anchor values
    ANCHOR_TOP = 1
    ANCHOR_MIDDLE = 3
    ANCHOR_BOTTOM = 4

    # AutoShape types ------------------

    SHAPE_10_POINT_STAR = 149
    SHAPE_12_POINT_STAR = 150
    SHAPE_16_POINT_STAR = 94
    SHAPE_24_POINT_STAR = 95
    SHAPE_32_POINT_STAR = 96
    SHAPE_4_POINT_STAR = 91
    SHAPE_5_POINT_STAR = 92
    SHAPE_6_POINT_STAR = 147
    SHAPE_7_POINT_STAR = 148
    SHAPE_8_POINT_STAR = 93
    SHAPE_ACTION_BUTTON_BACK_OR_PREVIOUS = 129
    SHAPE_ACTION_BUTTON_BEGINNING = 131
    SHAPE_ACTION_BUTTON_CUSTOM = 125
    SHAPE_ACTION_BUTTON_DOCUMENT = 134
    SHAPE_ACTION_BUTTON_END = 132
    SHAPE_ACTION_BUTTON_FORWARD_OR_NEXT = 130
    SHAPE_ACTION_BUTTON_HELP = 127
    SHAPE_ACTION_BUTTON_HOME = 126
    SHAPE_ACTION_BUTTON_INFORMATION = 128
    SHAPE_ACTION_BUTTON_MOVIE = 136
    SHAPE_ACTION_BUTTON_RETURN = 133
    SHAPE_ACTION_BUTTON_SOUND = 135
    SHAPE_ARC = 25
    SHAPE_BALLOON = 137
    SHAPE_BENT_ARROW = 41
    SHAPE_BENT_UP_ARROW = 44
    SHAPE_BEVEL = 15
    SHAPE_BLOCK_ARC = 20
    SHAPE_CAN = 13
    SHAPE_CHART_PLUS = 182
    SHAPE_CHART_STAR = 181
    SHAPE_CHART_X = 180
    SHAPE_CHEVRON = 52
    SHAPE_CHORD = 161
    SHAPE_CIRCULAR_ARROW = 60
    SHAPE_CLOUD = 179
    SHAPE_CLOUD_CALLOUT = 108
    SHAPE_CORNER = 162
    SHAPE_CORNER_TABS = 169
    SHAPE_CROSS = 11
    SHAPE_CUBE = 14
    SHAPE_CURVED_DOWN_ARROW = 48
    SHAPE_CURVED_DOWN_RIBBON = 100
    SHAPE_CURVED_LEFT_ARROW = 46
    SHAPE_CURVED_RIGHT_ARROW = 45
    SHAPE_CURVED_UP_ARROW = 47
    SHAPE_CURVED_UP_RIBBON = 99
    SHAPE_DECAGON = 144
    SHAPE_DIAGONAL_STRIPE = 141
    SHAPE_DIAMOND = 4
    SHAPE_DODECAGON = 146
    SHAPE_DONUT = 18
    SHAPE_DOUBLE_BRACE = 27
    SHAPE_DOUBLE_BRACKET = 26
    SHAPE_DOUBLE_WAVE = 104
    SHAPE_DOWN_ARROW = 36
    SHAPE_DOWN_ARROW_CALLOUT = 56
    SHAPE_DOWN_RIBBON = 98
    SHAPE_EXPLOSION1 = 89
    SHAPE_EXPLOSION2 = 90
    SHAPE_FLOWCHART_ALTERNATE_PROCESS = 62
    SHAPE_FLOWCHART_CARD = 75
    SHAPE_FLOWCHART_COLLATE = 79
    SHAPE_FLOWCHART_CONNECTOR = 73
    SHAPE_FLOWCHART_DATA = 64
    SHAPE_FLOWCHART_DECISION = 63
    SHAPE_FLOWCHART_DELAY = 84
    SHAPE_FLOWCHART_DIRECT_ACCESS_STORAGE = 87
    SHAPE_FLOWCHART_DISPLAY = 88
    SHAPE_FLOWCHART_DOCUMENT = 67
    SHAPE_FLOWCHART_EXTRACT = 81
    SHAPE_FLOWCHART_INTERNAL_STORAGE = 66
    SHAPE_FLOWCHART_MAGNETIC_DISK = 86
    SHAPE_FLOWCHART_MANUAL_INPUT = 71
    SHAPE_FLOWCHART_MANUAL_OPERATION = 72
    SHAPE_FLOWCHART_MERGE = 82
    SHAPE_FLOWCHART_MULTIDOCUMENT = 68
    SHAPE_FLOWCHART_OFFLINE_STORAGE = 139
    SHAPE_FLOWCHART_OFFPAGE_CONNECTOR = 74
    SHAPE_FLOWCHART_OR = 78
    SHAPE_FLOWCHART_PREDEFINED_PROCESS = 65
    SHAPE_FLOWCHART_PREPARATION = 70
    SHAPE_FLOWCHART_PROCESS = 61
    SHAPE_FLOWCHART_PUNCHED_TAPE = 76
    SHAPE_FLOWCHART_SEQUENTIAL_ACCESS_STORAGE = 85
    SHAPE_FLOWCHART_SORT = 80
    SHAPE_FLOWCHART_STORED_DATA = 83
    SHAPE_FLOWCHART_SUMMING_JUNCTION = 77
    SHAPE_FLOWCHART_TERMINATOR = 69
    SHAPE_FOLDED_CORNER = 16
    SHAPE_FRAME = 158
    SHAPE_FUNNEL = 174
    SHAPE_GEAR_6 = 172
    SHAPE_GEAR_9 = 173
    SHAPE_HALF_FRAME = 159
    SHAPE_HEART = 21
    SHAPE_HEPTAGON = 145
    SHAPE_HEXAGON = 10
    SHAPE_HORIZONTAL_SCROLL = 102
    SHAPE_ISOSCELES_TRIANGLE = 7
    SHAPE_LEFT_ARROW = 34
    SHAPE_LEFT_ARROW_CALLOUT = 54
    SHAPE_LEFT_BRACE = 31
    SHAPE_LEFT_BRACKET = 29
    SHAPE_LEFT_CIRCULAR_ARROW = 176
    SHAPE_LEFT_RIGHT_ARROW = 37
    SHAPE_LEFT_RIGHT_ARROW_CALLOUT = 57
    SHAPE_LEFT_RIGHT_CIRCULAR_ARROW = 177
    SHAPE_LEFT_RIGHT_RIBBON = 140
    SHAPE_LEFT_RIGHT_UP_ARROW = 40
    SHAPE_LEFT_UP_ARROW = 43
    SHAPE_LIGHTNING_BOLT = 22
    SHAPE_LINE_CALLOUT_1 = 109
    SHAPE_LINE_CALLOUT_1_ACCENT_BAR = 113
    SHAPE_LINE_CALLOUT_1_BORDER_AND_ACCENT_BAR = 121
    SHAPE_LINE_CALLOUT_1_NO_BORDER = 117
    SHAPE_LINE_CALLOUT_2 = 110
    SHAPE_LINE_CALLOUT_2_ACCENT_BAR = 114
    SHAPE_LINE_CALLOUT_2_BORDER_AND_ACCENT_BAR = 122
    SHAPE_LINE_CALLOUT_2_NO_BORDER = 118
    SHAPE_LINE_CALLOUT_3 = 111
    SHAPE_LINE_CALLOUT_3_ACCENT_BAR = 115
    SHAPE_LINE_CALLOUT_3_BORDER_AND_ACCENT_BAR = 123
    SHAPE_LINE_CALLOUT_3_NO_BORDER = 119
    SHAPE_LINE_CALLOUT_4 = 112
    SHAPE_LINE_CALLOUT_4_ACCENT_BAR = 116
    SHAPE_LINE_CALLOUT_4_BORDER_AND_ACCENT_BAR = 124
    SHAPE_LINE_CALLOUT_4_NO_BORDER = 120
    SHAPE_LINE_INVERSE = 183
    SHAPE_MATH_DIVIDE = 166
    SHAPE_MATH_EQUAL = 167
    SHAPE_MATH_MINUS = 164
    SHAPE_MATH_MULTIPLY = 165
    SHAPE_MATH_NOT_EQUAL = 168
    SHAPE_MATH_PLUS = 163
    SHAPE_MIXED = -2
    SHAPE_MOON = 24
    SHAPE_NON_ISOSCELES_TRAPEZOID = 143
    SHAPE_NOTCHED_RIGHT_ARROW = 50
    SHAPE_NOT_PRIMITIVE = 138
    SHAPE_NO_SYMBOL = 19
    SHAPE_OCTAGON = 6
    SHAPE_OVAL = 9
    SHAPE_OVAL_CALLOUT = 107
    SHAPE_PARALLELOGRAM = 2
    SHAPE_PENTAGON = 51
    SHAPE_PENTAGON = 51
    SHAPE_PIE = 142
    SHAPE_PIE_WEDGE = 175
    SHAPE_PLAQUE = 28
    SHAPE_PLAQUE_TABS = 171
    SHAPE_QUAD_ARROW = 39
    SHAPE_QUAD_ARROW_CALLOUT = 59
    SHAPE_RECTANGLE = 1
    SHAPE_RECTANGULAR_CALLOUT = 105
    SHAPE_REGULAR_PENTAGON = 12
    SHAPE_RIGHT_ARROW = 33
    SHAPE_RIGHT_ARROW_CALLOUT = 53
    SHAPE_RIGHT_BRACE = 32
    SHAPE_RIGHT_BRACKET = 30
    SHAPE_RIGHT_TRIANGLE = 8
    SHAPE_ROUNDED_RECTANGLE = 5
    SHAPE_ROUNDED_RECTANGULAR_CALLOUT = 106
    SHAPE_ROUND_1_RECTANGLE = 151
    SHAPE_ROUND_2_DIAG_RECTANGLE = 153
    SHAPE_ROUND_2_SAME_RECTANGLE = 152
    SHAPE_SMILEY_FACE = 17
    SHAPE_SNIP_1_RECTANGLE = 155
    SHAPE_SNIP_2_DIAG_RECTANGLE = 157
    SHAPE_SNIP_2_SAME_RECTANGLE = 156
    SHAPE_SNIP_ROUND_RECTANGLE = 154
    SHAPE_SQUARE_TABS = 170
    SHAPE_STRIPED_RIGHT_ARROW = 49
    SHAPE_SUN = 23
    SHAPE_SWOOSH_ARROW = 178
    SHAPE_TEAR = 160
    SHAPE_TRAPEZOID = 3
    SHAPE_UP_ARROW = 35
    SHAPE_UP_ARROW_CALLOUT = 55
    SHAPE_UP_DOWN_ARROW = 38
    SHAPE_UP_DOWN_ARROW_CALLOUT = 58
    SHAPE_UP_RIBBON = 97
    SHAPE_U_TURN_ARROW = 42
    SHAPE_VERTICAL_SCROLL = 101
    SHAPE_WAVE = 103

    # Shape Types ----------------------

    # shapes recognized so far
    AUTO_SHAPE = 1
    PICTURE = 13
    PLACEHOLDER = 14
    TEXT_BOX = 17
    TABLE = 19
    # shape type backlog (in implementation sequence)
    GROUP = 6
    CHART = 3
    # shapes left to be recognized
    CALLOUT = 2  # not sure why, but callout auto shapes are distinguished
    CANVAS = 20
    COMMENT = 4
    DIAGRAM = 21
    EMBEDDED_OLE_OBJECT = 7
    FORM_CONTROL = 8
    FREEFORM = 5
    IGX_GRAPHIC = 24  # SmartArt graphic
    INK = 22
    INK_COMMENT = 23
    LINE = 9
    LINKED_OLE_OBJECT = 10
    LINKED_PICTURE = 11
    MEDIA = 16
    OLE_CONTROL_OBJECT = 12
    SCRIPT_ANCHOR = 18
    SHAPE_TYPE_MIXED = -2
    TEXT_EFFECT = 15
    WEB_VIDEO = 26

    # Connector Shapes =====================

    # msoShapeMixed -2
    #     Return value only; indicates a combination of the other states.
    # msoShapeNotPrimitive 138
    #     Not supported.

    # 'bentConnector2'
    # 'bentConnector3'
    # 'bentConnector4'
    # 'bentConnector5'

    # 'curvedConnector2'
    # 'curvedConnector3'
    # 'curvedConnector4'
    # 'curvedConnector5'

    # 'line'

    # 'straightConnector1'
