from mcworldmanager.core import models


def test_MCAnalysedObject_without_any_errors():
    analysedObject = models.MCValidatesResultObject()
    assert not analysedObject.hasError()


def test_MCAnalysedObject_with_one_error():
    analysedObject = models.MCValidatesResultObject()
    analysedObject.append(models.CHUNK_NOT_CREATED)
    assert analysedObject.hasError()
    assert analysedObject.isErrorExists(models.CHUNK_NOT_CREATED)
    assert not analysedObject.isErrorExists(models.CHUNK_WRONG_LOCATED)
    assert analysedObject.isOneOfErrorsExists([models.CHUNK_WRONG_LOCATED, models.CHUNK_NOT_CREATED])
    assert not analysedObject.isOneOfErrorsExists([models.CHUNK_WRONG_LOCATED, models.CHUNK_TOO_MANY_ENTITIES])
    assert analysedObject.isOneOfErrorsExists([models.CHUNK_NOT_CREATED])
    assert not analysedObject.isOneOfErrorsExists([models.CHUNK_WRONG_LOCATED])


def test_MCAnalysedObject_with_one_of_error():
    analysedObject = models.MCValidatesResultObject()
    analysedObject.append(models.CHUNK_NOT_CREATED)
    assert analysedObject.isOneOfErrorsExists([models.CHUNK_NOT_CREATED])
    assert not analysedObject.isOneOfErrorsExists([models.CHUNK_WRONG_LOCATED])
    assert analysedObject.isOneOfErrorsExists(models.CHUNK_NOT_CREATED)
    assert not analysedObject.isOneOfErrorsExists(models.CHUNK_WRONG_LOCATED)
