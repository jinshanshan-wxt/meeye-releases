# Meeye 自定义图标包

个人自用分支。在上游 [yeyebbc/meeye-releases](https://github.com/yeyebbc/meeye-releases) 的正式包上换上自己的图标，用 GitHub Actions 打出一个签过名的 APK，放到 **Workflow Artifact** 里下载。这里不发 GitHub Release。

底包图标版权归原作者，许可见仓库 `LICENSE` 和上游说明。这个分支只给自己用。

## 定制了哪些图标

192px PNG 在 `icons/`，可编辑的 SVG 源也在同一目录。`icons/svg_render_check/` 只是 SVG 栅格化对照，不会打进 APK。

| 图标 | drawable | 怎么处理 |
| --- | --- | --- |
| Grok | `grok` | 新增 |
| Grok Bot | `grok_bot` | 新增。Activity 未核实，见下文 |
| X | `x_twitter` | 官方客户端从蓝色小鸟 `twitter` 改指向这张。包里已有的 `com.twitter.android` 条目会改 drawable |
| 飞牛 fnOS | `feiniu` | 新增。Activity 未核实 |
| Philips Sonicare | `philips_sonicare` | 新增。Activity 未核实 |
| Termius | `termius` | 补上原来指向了但不存在的图标，并加上现在的 MainActivity |
| PiliNara | `pilinara` | 新增（含 `.dev` 包名） |
| Venera | `venera` | 新增 |
| 雹 Hail | `hail` | 新增 |
| SenPlayer | `senplayer` | 新增。Activity 未核实 |
| 哔哩哔哩国际版（白） | `bilibili_white` | `com.bilibili.app.in` 从 `bilibili` 改指向这张。不是蓝色国际版 `com.bstar.intl` |
| Nrfr | `nrfr` | 新增 |
| Eskimo | `eskimo` | 新增。Activity 未核实 |
| Game Booster+ | `samsung_game_booster_plus` | 新增。Activity 请按本机核对 |
| DeepSeek | `deepseek` | 新增，白底蓝鲸 |
| DeepSeek 反色 | `deepseek_alt` | 备选，没有绑定组件 |
| Disney+ | `disney_plus` | 原位替换 |
| 美团 | `meituan` | 原位替换（白字、暖黄底） |
| 美团官方配色 | `meituan_alt` | 备选，黑字黄底，没有绑定组件 |
| Gemini | `google_gemini` | 原位换成现在的彩色星标 |
| Gemini 旧版 | `google_gemini_old` | 包里原来的图标留作备选 |
| 原神 | `genshin_a` | 已映射国服 `com.miHoYo.Yuanshen` 和国际服 `com.miHoYo.GenshinImpact`。光之门 |
| 原神备选 | `genshin_b`、`genshin_c` | 不绑定组件，可在图标包里手动选 |
| Samsung Expert RAW | `samsung_expert_raw` | 原位替换（Galaxy Store 图标重绘成 Meeye 风格） |
| Nothing X | `nothing_x` | 原位替换，并补上新的启动 Activity `host.MainActivity` |
| Canta | `canta` | 新增（Shizuku 卸载工具 `io.github.samolego.canta`） |
| ChatGPT | `chatgpt` | 原位替换：白底深色花形（官方图标形状不变）。包里原来的绿色版留作 `chatgpt_old`，没有绑定组件 |
| 什么值得买 | `shenmezhidemai` | 原位替换：白底红色「值」（官方图标的字形，去掉红圆）。原来的留作 `shenmezhidemai_old`，没有绑定组件 |
| Resplash | `resplash` | 原位替换 |
| TikTok | `tiktok` | 原位替换。`com.zhiliaoapp.musically` 和 `com.ss.android.ugc.trill` 从 `douyin` 改指向这张，抖音 `com.ss.android.ugc.aweme` 不动 |
| v2rayNG | `v2rayng`（包内原版） | 主图标仍是包里原来的白底 V。补上 `com.v2ray.ang` 和 `com.v2ray.ang.fdroid` 的新 Activity `ui.main.MainActivity`，并在图标列表里登记 |
| v2rayNG 官方 logo | `v2rayng_new` | 备选，官方 logo 形状不变、按包内原版的视觉中心居中，没有绑定组件 |
| Droid-ify 新版 | `droid_ify_alt` | 备选，包里原来的 `droid_ify` 不动，没有绑定组件 |
| 崩坏：星穹铁道 | （不动） | 继续用包内原来的 `benghuai_huoche` |

原神旧图标 `genshin_impact` 还在，只是官方客户端不再指向它。

## 还没核实的包名 / Activity

这些写在 `icons/appfilter_snippet.xml` 里。装好以后如果某个图标没生效，在电脑上查真正的启动 Activity，改 snippet，再推一次 `main`（或手动跑 workflow）：

```bash
adb shell cmd package resolve-activity --brief -c android.intent.category.LAUNCHER <包名>
```

需要核对的是：

- Grok Bot：`ai.x.grok.bot`（包名在 Play 上能对上，Activity 是猜的）
- 飞牛：`com.trim.app`（包名对得上，Activity 是猜的）
- Philips Sonicare：`com.philips.cdp.ohc.tuscany`（包名对得上，Activity 是猜的）
- Eskimo：`travel.eskimo.esim`（包名对得上，Activity 是猜的）
- SenPlayer：`com.wuziqi.SenPlayer`（包名来自第三方 APK 列表，启动 Activity 未知）
- Game Booster+：`com.samsung.android.game.honeyplayplus` 的 `ui.LaunchActivity`（请用上面的 adb 命令对一下）

`com.twitter.android` 的新增行会被构建脚本丢掉，避免和包里已经有的条目重复；已有条目会从 `twitter` 改成 `x_twitter`。要给 X 补一条包里没有的 Activity，直接改 `scripts/apply_icons.py` 里的过滤。


> 版本号：构建时把 versionCode 改成 900000（可用环境变量 `VERSION_CODE` 覆盖），versionName 改成「上游版本-custom」（如 `E-10.0-custom`），这样 Google Play 不会再提示"有更新"把它换回官方版。包名和签名不变。

## 下载 APK

1. 打开 [Actions](https://github.com/jinshanshan-wxt/meeye-releases/actions/workflows/build.yml)。
2. 选一次绿色的 **Build custom Meeye APK**。
   - 推到 `main`，并且改了 `icons/`、`scripts/` 或 workflow 本身，会自动构建。
   - 也可以点 **Run workflow** 手动跑。里面的 `apk_url` 留空就用上游最新正式包；填了就用那个 URL。上游接口失败或最新 Release 里没有 Meeye APK 时，回退到 tag `E-10.0` 的 `Meeye-E-10.0-c400-release.apk`。
3. 滚到该次运行页面最下面的 **Artifacts**，下载 `Meeye-custom-<底包版本>-<短 commit>`。
4. 下载下来是一个 zip，解压得到同名 `.apk`，传到手机安装。

Artifact 保留 90 天。过期了就再跑一次 workflow，不需要新的提交。这个仓库不会把 APK 发到 GitHub Releases，Obtainium 也跟不到这里。

构建要几分钟。底包里有六千多张 PNG，aapt2 是单线程重编。

## 必须先卸载官方 Meeye

这个包的签名和官方 Meeye 不一样。Android 不允许签名不同的包覆盖安装，所以要先卸掉官方版再装。卸载会清掉官方包里的本地数据。

配好下面的稳定密钥之后，以后每次构建的签名一致，自定义包之间可以互相覆盖更新。如果之前装过「临时密钥」打出来的包，换成稳定密钥后同样要先卸载一次。

## 签名

密钥库不要提交进仓库。workflow 在四个 Secrets 都存在时用它们签名；一个都没有就临时生成一把密钥，并在 Job Summary 里大声警告。只配了其中几个会直接失败，避免你以为已经用了稳定签名、其实签成了一次性的包。

在自己电脑上生成（Java 自带 `keytool`）：

```bash
keytool -genkeypair -v \
  -keystore meeye-custom.jks \
  -storetype PKCS12 \
  -alias meeye \
  -keyalg RSA \
  -keysize 2048 \
  -validity 10000 \
  -dname "CN=Meeye Custom, OU=Personal"
```

命令会问密钥库密码和密钥密码。两个可以设成同一个。生成后自己保管好 `meeye-custom.jks` 和密码（密码管理器或离线备份）。丢了就只能再卸载一次，重新用新密钥装。

把密钥库编成一行 base64：

```bash
# Linux
base64 -w0 meeye-custom.jks

# macOS
base64 -i meeye-custom.jks | tr -d '\n'
```

仓库 **Settings → Secrets and variables → Actions → New repository secret**，加这四个：

| Secret | 内容 |
| --- | --- |
| `KEYSTORE_BASE64` | 上面整段 base64 |
| `KEYSTORE_PASSWORD` | 密钥库密码 |
| `KEY_ALIAS` | `meeye`（或你在 `-alias` 里用的名字） |
| `KEY_PASSWORD` | 密钥密码 |

配好后重新跑 workflow。Summary 里的证书 SHA-256 每次应该一样。

## 本地构建

需要 Java 21（17 也行）、apktool 2.11.1、Android build-tools 里的 `zipalign` 和 `apksigner`。CI 用的就是这组版本。`rebuild.sh` 固定执行 `apktool b --use-aapt2`。2.12 及以后删掉了这个参数（aapt2 变成默认），不要换成那一版，除非同时改脚本。

```bash
scripts/rebuild.sh /path/to/Meeye-E-10.0-c400-release.apk icons dist/Meeye-custom.apk
```

稳定签名：

```bash
export KEYSTORE_FILE="$HOME/meeye-custom.jks"
export KEYSTORE_PASSWORD='你的密钥库密码'
export KEY_ALIAS=meeye
export KEY_PASSWORD='你的密钥密码'
scripts/rebuild.sh /path/to/base.apk icons dist/Meeye-custom.apk
```

没设置 `KEYSTORE_FILE` 时，脚本会在临时目录里生成一把一次性密钥并在终端里警告。`APKTOOL_JAR` 可以指向 apktool 的 jar；不设的话用 PATH 上的 `apktool`。

`scripts/download_base.py` 和 CI 用同一套规则下载底包（`--dry-run` 只解析 URL）。

## 目录

- `icons/`：最终 PNG、SVG、`appfilter_snippet.xml`、`drawable_snippet.xml`
- `scripts/apply_icons.py`：把 PNG 拷进 `res/drawable-nodpi`，改 appfilter 指向，把新条目写进 `assets/` 和 `res/xml/` 两份 `appfilter.xml`，并在两份 `drawable.xml` 的 Latest 分类里加上新图标。原来的 `google_gemini.png` 会先复制成 `google_gemini_old.png`
- `scripts/rebuild.sh`：`apktool d` → apply → `apktool b --use-aapt2` → `zipalign` → `apksigner` → 校验 v1/v2/v3
- `tools/design/`：重新画图标的脚本（`build_icons.py`、`meeye_style.py` 等）。CI 不用它们。它们依赖一个本地工作目录里的 `resmap.json`、`apk/`、`refs/`，用环境变量 `MEEYE_ROOT` 指向那个目录（默认是本仓库根目录）

图标绘制细节见 `icons/README.md`。
