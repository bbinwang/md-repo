# Ref2VA 全参考提示词示例结构图：咖啡店 · 萨摩耶 · 双角色对白

> 学习产出：基于[全参考模式（Full-Reference）改写输出格式指南](../video-prompt-writing-guide-ref.md)整理的示例。
> 场景：咖啡店情景喜剧，萨摩耶扑曲奇，双角色三镜头对白，罐头笑声收尾（约 6 秒）。

## 输入素材

| 素材 | 内容 | 用途 |
|---|---|---|
| Picture 1 | 咖啡店实景 | 场景主体 Subject 1 |
| Picture 2 / 3 / 4 | 白色萨摩耶（多角度） | 角色主体 Subject 2 |
| Video 1 | 金发女子 | 说话人 S1 · Subject 3 |
| Video 2 | 灰帽衫男子 | 说话人 S2 · Subject 4 |
| Audio 1 | 英文说话人声 | S1 音色参考（不复制原信号） |

## 结构图 1：整体结构（素材 → 主体 → 镜头 → 声音）

```mermaid
flowchart TB
subgraph IN["输入素材"]
direction LR
P1["Picture 1<br/>咖啡店实景"]
P234["Picture 2 / 3 / 4<br/>白色萨摩耶"]
V1["Video 1<br/>金发女子"]
V2["Video 2<br/>灰帽衫男子"]
A1["Audio 1<br/>英文说话人声"]
end
subgraph SUB["Subjects 主体 · 全镜头 fully_preserved"]
direction LR
SUB1["Subject 1 咖啡店场景<br/>砖墙 / 橙沙发 / 花纹抱枕<br/>霓虹灯 / 木茶几"]
SUB2["Subject 2 萨摩耶<br/>厚白毛 / 尖耳 / 黑鼻 / 卷尾"]
SUB3["Subject 3 说话人S1 金发女子<br/>长金发 / 浅粉衬衫 / 卷袖"]
SUB4["Subject 4 说话人S2 褐发男子<br/>短卷褐发 / 深灰帽衫 / 抽绳"]
end
subgraph SHOT["Shot 结构 · 真实多机位情景喜剧 · 暖光"]
direction TB
SH1["Shot 1｜00:00 中景<br/>SUB3 持巧克力曲奇坐沙发，SUB4 牵 SUB2 自左入场<br/>狗扑向曲奇，牵绳绷紧，SUB3 缩手护饼<br/>S1 台词：Hey! Watch your dog!<br/>音色取自 Audio 1 · 轻懊恼"]
SH2["Shot 2｜00:03 近景 SUB4<br/>SUB4 坐到 SUB3 身旁，将 SUB2 抱稳<br/>S2 台词：He just likes cookies more than me.<br/>轻松年轻男声 · 歉意微笑 · 抚摸狗"]
SH3["Shot 3｜00:05 近景 SUB3<br/>神情软化，看向萨摩耶<br/>S1 台词：Well, he has good taste at least.<br/>同 Audio 1 音色 · 笑意 · 举饼致意"]
end
subgraph AUD["声音层"]
direction LR
ROOM["房间底噪<br/>咖啡店室内 room tone 全程持续"]
VOX["对白<br/>SUB3 音色参考 Audio 1 不复制原信号<br/>SUB4 口语化年轻男声"]
LAF["罐头笑声<br/>Shot 3 台词后立刻接入<br/>延续至最后一帧"]
MUS["非叙事音乐：N/A"]
end
OUT["目标视频<br/>SUB3 在 SUB1 吃曲奇 → SUB4 带 SUB2 入场<br/>狗扑食 → 三镜头对白 → 罐头笑声收尾"]
P1 --> SUB1
P234 --> SUB2
V1 --> SUB3
V2 --> SUB4
A1 -.->|音色参考| SUB3
SUB1 --> SH1 & SH2 & SH3
SUB2 --> SH1 & SH2
SUB3 --> SH1 & SH2 & SH3
SUB4 --> SH1 & SH2
SH1 --> SH2 --> SH3 --> OUT
A1 --> VOX
SH3 --> LAF
SHOT --> AUD --> OUT
classDef subj fill:#fff4e6,stroke:#e8890c,color:#333
classDef shot fill:#eef6ff,stroke:#2b7cd3,color:#333
classDef aud fill:#f3e8ff,stroke:#7c3aed,color:#333
class SUB1,SUB2,SUB3,SUB4 subj
class SH1,SH2,SH3 shot
class ROOM,VOX,LAF,MUS aud
```

## 结构图 2：时间线（镜头推进 + 声音事件）

```mermaid
sequenceDiagram
autonumber
participant SCENE as 场景 Subject 1 咖啡店
participant S1 as Subject 3 金发女子 说话人S1
participant S2 as Subject 4 男子 说话人S2
participant DOG as Subject 2 萨摩耶
participant SND as 声音层
Note over SCENE,SND: Shot 1 中景 起始 00:00
SCENE->>S1: 持巧克力曲奇坐在橙色沙发上
S2->>DOG: 牵绳自左侧入场
DOG->>S1: 扑向曲奇 牵绳绷紧
S1-->>SND: 台词 Hey Watch your dog 音色参考 Audio 1 语气轻懊恼
S2->>DOG: 把狗拉回
Note over SCENE,SND: Shot 2 近景 S2 00:03
S2->>DOG: 抱住狗 坐到 S1 身旁
S2-->>SND: 台词 He just likes cookies more than me 轻松年轻男声
Note over SCENE,SND: Shot 3 近景 S1 00:05
S1->>DOG: 看向狗 神情软化
S1-->>SND: 台词 Well he has good taste at least 带笑意
SND-->>SCENE: 罐头笑声立即接入 延续至最后一帧
Note over SND: 咖啡店室内 room tone 全程垫底 非叙事音乐无
```

## 与六段式输出的对应

| 六段式小节 | 对应结构图 1 部分 |
|---|---|
| `subject_definitions` | Subjects 层（SUB1–SUB4，含素材来源） |
| `summary` | 顶层箭头流：输入素材 → 目标视频 |
| `retention_analysis` | 各主体的 fully_preserved 标注 |
| `detailed_description` | Shot 层（SH1 → SH2 → SH3 时间推进） |
| `overall_soundscape` | 声音层（ROOM / VOX / LAF） |
| `non_diegetic_music` | MUS（N/A） |
