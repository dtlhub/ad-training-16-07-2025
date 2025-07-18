# AD Training 16.07.2025

[![check-services](https://github.com/dtlhub/ad-training-16-07-2025/actions/workflows/check-services.yml/badge.svg?branch=master&event=push)](https://github.com/dtlhub/ad-training-16-07-2025/actions/workflows/check-services.yml)

Attack-Defense CTF training for high-school students, which was developed by members of [dtl](https://ctftime.org/team/157017) and [Rop Runners](https://ctftime.org/team/279418) teams.

![Top of the scoreboard](./screenshots/top.png)

## Services

| Service                             | Language   | Vulns | Authors |
| ----------------------------------- | ---------- | ----- | ------- |
| [battlebots](/services/battlebots/) | C          | got rw via integer overflow; overwrite printf to scanf; rop to system | [@FlexMaster420](https://t.me/FlexMaster420) |
| [crmka](/services/crmka/)           | JavaScript | Chain: bypass jwt authentication via logic bug in exception handler + insufficient filtering in dynamical import leads to RCE | @bytehope |
| [enchaintix](/services/enchaintix/) | Python     | Prompt injection, SQL injection | @c3N1T3Lb |
| [flagbin](/services/flagbin/)       | C          | Path traversal via retrieve flag; read maps - ../../proc/self/maps; read mem - ../../proc/self/mem | [@FlexMaster420](https://t.me/FlexMaster420) |
| [nevalashka](/services/nevalashka/) | PHP        | SQL injection, auth bypass, IDOR | @vanindm |

## Infrastructure

- DevOps: [@LeKSuS](https://github.com/LeKSuS-04)
- Checksystem: [ForcAD](https://github.com/pomo-mondreganto/ForcAD)

## Writeups

- [battlebots](/sploits/battlebots/)
- [crmka](/sploits/crmka/)
- [enchaintix](/sploits/enchaintix/)
- [flagbin](/sploits/flagbin/)
- [nevalashka](/sploits/nevalashka/)
