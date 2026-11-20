# New Meeye-style icons
PNG = native 192x192 RGBA (pack's own squircle mask, rim overlay and outer shadow reused from the APK; glyph shadow/gradients fitted to the pack).
SVG = editable source (squircle + gradients + glyph; outer-shadow/rim are approximations, see PNG for the exact render). 
Drawable names: grok grok_bot x_twitter feiniu philips_sonicare termius pilinara venera hail senplayer nrfr eskimo samsung_game_booster_plus deepseek bilibili_white (new);
disney_plus meituan (replaced in place); genshin_a genshin_b genshin_c (new, pick one; a is mapped; original pack genshin_impact kept as alt; HSR left as in the pack); deepseek_alt meituan_alt (extra options); google_gemini replaced in place (old copy = google_gemini_old).
Rebuild: tools/rebuild.sh <orig.apk> new_icons out.apk  (apktool d -> apply_icons.py -> apktool b --use-aapt2 -> zipalign -> apksigner)

Batch 8: canta (new); v2rayng samsung_expert_raw nothing_x droid_ify resplash tiktok replace the pack's drawables in place (apps already mapped there).
