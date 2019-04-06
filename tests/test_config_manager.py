from mcworldmanager.config_manager import configure_conf


def test_load_default_config():
    config = configure_conf()
    assert config
    assert "report" in config
    assert "MINIMAL" == config["report"]["details_level"]
