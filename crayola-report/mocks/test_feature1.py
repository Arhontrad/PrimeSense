import logging

logger = logging.getLogger("crayola")

class TestFeature1(object):
    def test_foo(self):
        logger.info("i am foo")

    def test_bar(self):
        logger.info("i am bar")
        assert False

class TestFeature3(object):
    def test_foo(self):
        logger.info("i am foo")
        logger.warn("oh my %d", 7)
        logger.error("oh no! %d", 5)

    def test_bar(self):
        logger.info("i am bar")
