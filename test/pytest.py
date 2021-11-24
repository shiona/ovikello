import logging

import pytest
from pytest_mock import MockerFixture
from unittest.mock import ANY

from ptbtest import ChatGenerator
from ptbtest import MessageGenerator
from ptbtest import Mockbot
from ptbtest import UserGenerator

#from bot import Updater, DoorbellBot, CHECK
import bot
import led

@pytest.fixture
def ovikello(mocker: MockerFixture):
    mockbot = Mockbot()

    def mock_create_updater(it, _):
        it.updater = bot.Updater(bot=mockbot)

    mocker.patch('bot.DoorbellBot.create_updater', mock_create_updater)

    led = mocker.MagicMock()


    ovikello = bot.DoorbellBot('fake_token', led)
    stop = mocker.patch.object(ovikello, 'stop')

    # Give the test case a way to access the mock objects
    # so that it can check for calls
    ovikello.mockled = led
    ovikello.mockbot = mockbot
    ovikello.mockstop = stop

    # Bypass the DoorbellBots wrapper to fake
    ovikello.updater.start_polling()

    yield ovikello

    ovikello.updater.stop()


def test_led(mocker: MockerFixture) -> None:
    mocknp = mocker.patch('led.Adafruit_NeoPixel')
    mockbegin = mocker.patch.object(mocknp.return_value, 'begin')
    mocksetpixel = mocker.patch.object(mocknp.return_value, 'setPixelColor')

    l = led.Led(2, 18)

    mocknp.assert_called_once_with(18, 2, ANY, ANY, ANY, ANY)
    mockbegin.assert_called_once()
    mocksetpixel.assert_any_call(0, led.BLACK)
    mocksetpixel.assert_any_call(1, led.BLACK)


def test_bot_led_call(mocker: MockerFixture, ovikello) -> None:
    ug = UserGenerator()
    user = ug.get_user(first_name="Test", last_name="The Bot")
    chat = ovikello.mockbot.cg.get_chat(user=user)

    # NOTE: parse_mode is important
    update = ovikello.mockbot.mg.get_message(user=user, chat=chat, text="/ovikello k-laiva", parse_mode = "HTML")
    ovikello.mockbot.insertUpdate(update)
    assert len(ovikello.mockbot.sent_messages) == 1
    sent = ovikello.mockbot.sent_messages[0]
    assert sent['method'] == "sendMessage"
    assert sent['text'] == bot.CHECK

    ovikello.mockled.alert.assert_called_once()


def test_bot_upgrade_call_success(mocker: MockerFixture, ovikello) -> None:
    ug = UserGenerator()
    user = ug.get_user(first_name="Test", last_name="The Bot")
    chat = ovikello.mockbot.cg.get_chat(user=user)

    # Mock a successful upgrade
    mockota = mocker.patch('ota.OTA')
    mockotarun = mocker.patch.object(mockota.return_value, 'run', return_value=True)

    # NOTE: parse_mode is important
    update = ovikello.mockbot.mg.get_message(user=user, chat=chat, text="/upgrade", parse_mode = "HTML")
    ovikello.mockbot.insertUpdate(update)
    assert len(ovikello.mockbot.sent_messages) == 2
    first = ovikello.mockbot.sent_messages[0]
    snd = ovikello.mockbot.sent_messages[1]
    assert first['method'] == "sendMessage"
    assert first['text'] == bot.CONSTRUCTION_SIGN
    assert snd['method'] == "editMessageText"
    assert snd['text'] == bot.CHECK
    assert first['chat_id'] == snd['chat_id']

    mockotarun.assert_called_once()
    ovikello.mockstop.assert_called_once()


def test_bot_upgrade_call_no_update(mocker: MockerFixture, ovikello) -> None:
    ug = UserGenerator()
    user = ug.get_user(first_name="Test", last_name="The Bot")
    chat = ovikello.mockbot.cg.get_chat(user=user)

    # Mock a failed upgrade due to no newer version
    mockota = mocker.patch('ota.OTA')
    mockotarun = mocker.patch.object(mockota.return_value, 'run', return_value=False)

    # NOTE: parse_mode is important
    update = ovikello.mockbot.mg.get_message(user=user, chat=chat, text="/upgrade", parse_mode = "HTML")
    ovikello.mockbot.insertUpdate(update)
    assert len(ovikello.mockbot.sent_messages) == 2
    first = ovikello.mockbot.sent_messages[0]
    snd = ovikello.mockbot.sent_messages[1]
    assert first['method'] == "sendMessage"
    assert first['text'] == bot.CONSTRUCTION_SIGN
    assert snd['method'] == "editMessageText"
    assert snd['text'] == bot.CROSS
    assert first['chat_id'] == snd['chat_id']

    mockotarun.assert_called_once()
    ovikello.mockstop.assert_not_called()
