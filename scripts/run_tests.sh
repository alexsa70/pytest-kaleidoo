#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────────────────────
# run_tests.sh — Test execution wrapper for pytest-kaleidoo
#
# Usage:
#   ./scripts/run_tests.sh [options] [extra pytest args]
#
# Options:
#   --allure-dir=<dir>      Allure results directory  (default: allure-results)
#   --test=<path>           Test path to run           (default: tests/api)
#   --m=<marker>            Pytest marker filter       (e.g. smoke, regression)
#   --parallel=<n>          Workers (auto or number)   (default: off)
#   --reruns=<n>            Retry failed tests N times (default: 0)
#   --testmo                Submit results to Testmo
#   --env=<environment>     Environment: qa|prod|onprem (default: qa)
# ──────────────────────────────────────────────────────────────────────────────
set -euo pipefail

# ── Defaults ──────────────────────────────────────────────────────────────────
ALLURE_DIR="allure-results"
TEST_PATH="tests/api"
MARKER=""
PARALLEL=""
RERUNS=0
ENABLE_TESTMO=false
ENVIRONMENT="${ENVIRONMENT:-qa}"
EXTRA_ARGS=()

# ── Parse arguments ───────────────────────────────────────────────────────────
for arg in "$@"; do
    case $arg in
        --allure-dir=*)  ALLURE_DIR="${arg#*=}" ;;
        --test=*)        TEST_PATH="${arg#*=}" ;;
        --m=*)           MARKER="${arg#*=}" ;;
        --parallel=*)    PARALLEL="${arg#*=}" ;;
        --reruns=*)      RERUNS="${arg#*=}" ;;
        --env=*)         ENVIRONMENT="${arg#*=}" ;;
        --testmo)        ENABLE_TESTMO=true ;;
        *)               EXTRA_ARGS+=("$arg") ;;
    esac
done

# ── Load .env if running locally ──────────────────────────────────────────────
if [ "${CI:-false}" != "true" ] && [ -f ".env" ]; then
    echo "Loading .env..."
    set -a; source .env; set +a
fi

# ── Clean previous results (keep history) ─────────────────────────────────────
if [ -d "$ALLURE_DIR" ]; then
    find "$ALLURE_DIR" -mindepth 1 -not -path "*/$ALLURE_DIR/history*" -delete
fi
mkdir -p "$ALLURE_DIR"

# ── Build pytest command ───────────────────────────────────────────────────────
PYTEST_CMD="python -m pytest $TEST_PATH --alluredir=$ALLURE_DIR --tb=short"

[ -n "$MARKER" ]   && PYTEST_CMD+=" -m $MARKER"
[ -n "$PARALLEL" ] && PYTEST_CMD+=" -n $PARALLEL"
[ "$RERUNS" -gt 0 ] && PYTEST_CMD+=" --reruns=$RERUNS"
[ ${#EXTRA_ARGS[@]} -gt 0 ] && PYTEST_CMD+=" ${EXTRA_ARGS[*]}"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Environment : $ENVIRONMENT"
echo "Test path   : $TEST_PATH"
echo "Marker      : ${MARKER:-<all>}"
echo "Allure dir  : $ALLURE_DIR"
echo "Command     : $PYTEST_CMD"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# ── Run tests ─────────────────────────────────────────────────────────────────
set +e
eval "$PYTEST_CMD"
EXIT_CODE=$?
set -e

# ── Generate environment.properties for Allure ────────────────────────────────
BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")
COMMIT_ID=$(git rev-parse HEAD 2>/dev/null || echo "unknown")
COMMIT_MSG=$(git log -1 --pretty=%s 2>/dev/null || echo "unknown")

cat > "$ALLURE_DIR/environment.properties" <<EOF
ENVIRONMENT=${ENVIRONMENT}
BRANCH=${BRANCH}
COMMIT_ID=${COMMIT_ID}
COMMIT_MESSAGE=${COMMIT_MSG}
API_URL=${API_HTTP_CLIENT_URL:-}
EOF

# ── Testmo submission ─────────────────────────────────────────────────────────
if [ "$ENABLE_TESTMO" = true ]; then
    echo "Submitting results to Testmo..."
    testmo automation:run:submit \
        --instance "https://kaleidoo.testmo.net" \
        --project-id 1 \
        --name "API Tests — ${ENVIRONMENT}" \
        --source "api-${ENVIRONMENT}" \
        --results "$ALLURE_DIR/*.xml" \
        -- echo "done"
fi

# ── Generate local Allure report (non-CI only) ────────────────────────────────
if [ "${CI:-false}" != "true" ]; then
    if command -v allure &>/dev/null; then
        allure generate "$ALLURE_DIR" -o allure-report --clean
        allure open allure-report
    else
        echo "Allure CLI not found. Run: npm install -g allure-commandline"
    fi
fi

exit $EXIT_CODE
