#!/usr/bin/env bash
# Allure 报告：生成 + 打开
#
# 用法:
#   ./scripts/allure_report.sh                       # 从现有 allure-results 生成并打开
#   ./scripts/allure_report.sh <pytest参数...>       # 先跑测试(自动加 --alluredir)再生成并打开
#
# 示例:
#   ./scripts/allure_report.sh Testcase/Auto_pre/DistService/test_DistTeam*.py -s
#
# 说明: 报告必须通过 HTTP 打开（file:// 下 fetch 被拦截会一直 loading）
set -e

cd "$(dirname "$0")/.."

# 默认自动选一个空闲端口；可用环境变量 ALLURE_PORT 指定
PORT="${ALLURE_PORT:-$(python3 -c 'import socket; s=socket.socket(); s.bind(("",0)); print(s.getsockname()[1]); s.close()')}"

TOOL_DIR="$HOME/.allure-toolchain"
JRE_DIR="$TOOL_DIR/zulu17.68.17-ca-fx-jre17.0.20-macosx_x64/Contents/Home"
ALLURE="$TOOL_DIR/allure-2.30.0/bin/allure"

if command -v allure >/dev/null 2>&1; then
  # 系统已装 allure 则优先使用
  ALLURE="allure"
  unset JAVA_HOME
else
  export JAVA_HOME="$JRE_DIR"
fi

# 传了 pytest 参数就先跑测试（带 --alluredir 生成结果）
if [ $# -gt 0 ]; then
  rm -rf allure-results
  .venv/bin/python3 -m pytest "$@" --alluredir=allure-results -q --tb=short
fi

"$ALLURE" generate allure-results -o allure-report --clean

# 起本地 HTTP 服务（后台、脱离），确认起来后再异步打开浏览器
(
  cd allure-report
  nohup python3 -m http.server "$PORT" </dev/null >/dev/null 2>&1 &
  disown
)
for _ in $(seq 1 20); do
  if curl -s -o /dev/null --max-time 1 "http://localhost:$PORT/"; then
    break
  fi
  sleep 0.5
done
nohup open "http://localhost:$PORT" >/dev/null 2>&1 &
exit 0
