import logging
from aiogram.utils.exceptions import (Unauthorized, InvalidQueryID, TelegramAPIError,
                                      CantDemoteChatCreator, MessageNotModified, MessageToDeleteNotFound,
                                      MessageTextIsEmpty, RetryAfter,
                                      CantParseEntities, MessageCantBeDeleted)


from loader import dp, my_logger


@dp.errors_handler()
async def errors_handler(update, exception):
    """
    Exceptions handler. Catches all exceptions within task factory tasks.
    :param dispatcher:
    :param update:
    :param exception:
    :return: stdout logging
    """

    if isinstance(exception, CantDemoteChatCreator):
        my_logger.exception("Can't demote chat creator")
        return True

    if isinstance(exception, MessageNotModified):
        my_logger.exception('Message is not modified')
        return True
    if isinstance(exception, MessageCantBeDeleted):
        my_logger.exception('Message cant be deleted')
        return True

    if isinstance(exception, MessageToDeleteNotFound):
        my_logger.exception('Message to delete not found')
        return True

    if isinstance(exception, MessageTextIsEmpty):
        my_logger.exception('MessageTextIsEmpty')
        return True

    if isinstance(exception, Unauthorized):
        my_logger.exception(f'Unauthorized: {exception}')
        return True

    if isinstance(exception, InvalidQueryID):
        my_logger.exception(f'InvalidQueryID: {exception} \nUpdate: {update}')
        return True

    if isinstance(exception, TelegramAPIError):
        my_logger.exception(f'TelegramAPIError: {exception} \nUpdate: {update}')
        return True
    if isinstance(exception, RetryAfter):
        my_logger.exception(f'RetryAfter: {exception} \nUpdate: {update}')
        return True
    if isinstance(exception, CantParseEntities):
        my_logger.exception(f'CantParseEntities: {exception} \nUpdate: {update}')
        return True
    
    logging.exception(f'Update: {update} \n{exception}')
    logging.exception(exception)