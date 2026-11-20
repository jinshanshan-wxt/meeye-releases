# New Meeye-style icons (19 + 2 alternates + 2 official-art games)
PNG = native 192x192 RGBA (pack's own squircle mask, rim overlay and outer shadow reused from the APK; glyph shadow/gradients fitted to the pack).
SVG = editable source (squircle + gradients + glyph; outer-shadow/rim are approximations, see PNG for the exact render). 
Drawable names: grok grok_bot x_twitter feiniu philips_sonicare termius pilinara venera hail senplayer nrfr eskimo samsung_game_booster_plus deepseek bilibili_white (new);
disney_plus meituan (replaced in place); genshin_a genshin_b genshin_c (new, pick one; a is mapped; original pack genshin_impact kept as alt; HSR left as in the pack); deepseek_alt meituan_alt (extra options); google_gemini replaced in place (old copy = google_gemini_old).
`svg_render_check/` is an SVG raster comparison only; those PNGs are not packed.
Rebuild: scripts/rebuild.sh <orig.apk> icons out.apk  (apktool d -> scripts/apply_icons.py -> apktool b --use-aapt2 -> zipalign -> apksigner). CI runs that same script. See the repo README.
