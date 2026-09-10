from typing import Literal, get_args

type FontFlavor = Literal[
    'latin',
    'zh_hans',
    'zh_hant',
    'ja',
    'ko',
]
FONT_FLAVORS = list[FontFlavor](get_args(FontFlavor.__value__))
