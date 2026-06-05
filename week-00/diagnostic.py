def parse_dotenv(text: str) -> dict[str, str]:
    """Parse KEY=VALUE lines, skipping blank lines and # comments."""
    result = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if '=' in line:
            key, _, value = line.partition('=')
            result[key.strip()] = value.strip()
    return result


def test_basic():
    env = parse_dotenv("HOST=localhost\nPORT=8080")
    assert env == {"HOST": "localhost", "PORT": "8080"}, env

def test_skips_blanks_and_comments():
    env = parse_dotenv("# comment\n\nKEY=value")
    assert env == {"KEY": "value"}, env

def test_value_contains_equals():
    # partition('=') splits on the first '=' only, so URLs with query strings survive intact
    env = parse_dotenv("URL=http://example.com?a=1&b=2")
    assert env == {"URL": "http://example.com?a=1&b=2"}, env


if __name__ == "__main__":
    test_basic()
    test_skips_blanks_and_comments()
    test_value_contains_equals()
    print("All 3 tests passed.")
