from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor

TOKEN = '1659069813:AAGlRZ2pqTT65ngH_qUuHph-z3LqLvs7UkU'

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class Form(StatesGroup):
    square_ = State()
    number_floors_ = State()
    type_found_ = State()
    material_ = State()
    type_roof_ = State()


class Inline:
    start_inline = types.InlineKeyboardMarkup()
    start_button = types.InlineKeyboardButton(text='Start', callback_data='start')
    start_inline.insert(start_button)

    restart_inline = types.InlineKeyboardMarkup()
    restart_button = types.InlineKeyboardButton(text='Рассчитать заново', callback_data='start')
    restart_inline.insert(restart_button)

    restart_inline_ = types.InlineKeyboardMarkup()
    restart_button_ = types.InlineKeyboardButton(text='Ок, понял 👌', callback_data='start')
    restart_inline_.insert(restart_button_)

    foundation_inline = types.InlineKeyboardMarkup()
    tape_button = types.InlineKeyboardButton(text='Ленточный', callback_data='tape')
    pile_button = types.InlineKeyboardButton(text='Свайный', callback_data='pile')
    plate_button = types.InlineKeyboardButton(text='Плитный', callback_data='plate')
    foundation_inline.insert(tape_button)
    foundation_inline.insert(pile_button)
    foundation_inline.add(plate_button)

    material_inline = types.InlineKeyboardMarkup()
    bar_button = types.InlineKeyboardButton(text='Брус', callback_data='bar')
    aerated_concrete_block_button = types.InlineKeyboardButton(text='Газобетон', callback_data='ac_block')
    ceramic_block_button = types.InlineKeyboardButton(text='Керамический блок', callback_data='ceramic_block')
    brick_button = types.InlineKeyboardButton(text='Кирпич', callback_data='brick')
    door_button = types.InlineKeyboardButton(text='Деревянный каркас', callback_data='door')
    material_inline.insert(bar_button)
    material_inline.insert(ceramic_block_button)
    material_inline.add(aerated_concrete_block_button)
    material_inline.insert(brick_button)
    material_inline.add(door_button)

    roof_inline = types.InlineKeyboardMarkup()
    sheet_button = types.InlineKeyboardButton(text='Листовые материалы', callback_data='sheet')
    flexible_button = types.InlineKeyboardButton(text='Гибкая кровля', callback_data='flex')
    ceramic_roof_button = types.InlineKeyboardButton(text='Штучные материалы', callback_data='ceramic_roof')
    roof_inline.insert(sheet_button)
    roof_inline.add(flexible_button)
    roof_inline.add(ceramic_roof_button)

    result_inline = types.InlineKeyboardMarkup()
    result_button = types.InlineKeyboardButton(text='Подвести итоги', callback_data='result')
    result_inline.insert(result_button)


@dp.message_handler()
async def start(msg: types.Message):
    print(msg.from_user.full_name)
    await bot.send_message(msg.from_user.id, 'Привет!\nТут ты сможешь рассчитать примерную сумму затрат на '
                                             'строительство загородного дома 🏠\nНачнем?)',
                           reply_markup=Inline.start_inline)


@dp.callback_query_handler(lambda c: c.data == 'start')
async def square(call: types.CallbackQuery):
    await bot.send_message(call.from_user.id, 'Какую площадь в м² на участке будет занимать дом?\n')
    await Form.square_.set()


@dp.message_handler(state=Form.square_)
async def numbers(msg: types.Message, state: FSMContext):
    k = 0
    try:
        int(msg.text)
    except ValueError:
        await bot.send_message(msg.from_user.id, 'Введите площадь в квадратных метрах, единицы измерения указывать не '
                                                 'нужно\nПример: 210', reply_markup=Inline.restart_inline_)
        await state.finish()
        k = 1
    if k == 0:
        async with state.proxy() as data:
            data['square_'] = msg.text
        await Form.next()
        await bot.send_message(msg.from_user.id, 'А сколько этажей планируешь?')


@dp.message_handler(state=Form.number_floors_)
async def found(msg: types.Message, state: FSMContext):
    k = 0
    try:
        int(msg.text)
    except ValueError:
        await bot.send_message(msg.from_user.id, 'Введите количество этажей, единицы измерения указывать не '
                                                 'нужно\nПример: 2', reply_markup=Inline.restart_inline_)
        await state.finish()
        k = 1
    if k == 0:
        async with state.proxy() as data:
            data['number_floors_'] = msg.text
        await Form.next()
        await bot.send_message(msg.from_user.id, 'Какой фундамент хочешь?', reply_markup=Inline.foundation_inline)


@dp.callback_query_handler(lambda c: c.data == 'tape', state=Form.type_found_)
async def tape(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['type_found_'] = 1
    await Form.next()
    await bot.send_message(call.from_user.id, 'А теперь выбери основной материал дома',
                           reply_markup=Inline.material_inline)


@dp.callback_query_handler(lambda c: c.data == 'pile', state=Form.type_found_)
async def pile(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['type_found_'] = 2
    await Form.next()
    await bot.send_message(call.from_user.id, 'А теперь выбери основной материал дома',
                           reply_markup=Inline.material_inline)


@dp.callback_query_handler(lambda c: c.data == 'plate', state=Form.type_found_)
async def plate(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['type_found_'] = 3
    await Form.next()
    await bot.send_message(call.from_user.id, 'А теперь выбери основной материал дома',
                           reply_markup=Inline.material_inline)


@dp.callback_query_handler(lambda c: c.data == 'bar', state=Form.material_)
async def bar(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['material_'] = 1
    await Form.next()
    await bot.send_message(call.from_user.id, 'И последнее\nКакого типа будет кровля?',
                           reply_markup=Inline.roof_inline)


@dp.callback_query_handler(lambda c: c.data == 'ac_block', state=Form.material_)
async def ac_block(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['material_'] = 2
    await Form.next()
    await bot.send_message(call.from_user.id, 'И последнее\nКакого типа будет кровля?',
                           reply_markup=Inline.roof_inline)


@dp.callback_query_handler(lambda c: c.data == 'ceramic_block', state=Form.material_)
async def ceramick_block(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['material_'] = 3
    await Form.next()
    await bot.send_message(call.from_user.id, 'И последнее\nКакого типа будет кровля?',
                           reply_markup=Inline.roof_inline)


@dp.callback_query_handler(lambda c: c.data == 'brick', state=Form.material_)
async def brick(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['material_'] = 4
    await Form.next()
    await bot.send_message(call.from_user.id, 'И последнее\nКакого типа будет кровля?',
                           reply_markup=Inline.roof_inline)


@dp.callback_query_handler(lambda c: c.data == 'door', state=Form.material_)
async def door(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['material_'] = 5
    await Form.next()
    await bot.send_message(call.from_user.id, 'И последнее\nКакого типа будет кровля?',
                           reply_markup=Inline.roof_inline)


@dp.callback_query_handler(lambda c: c.data == 'sheet', state=Form.type_roof_)
async def sheet(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['type_roof_'] = 1
    await bot.send_message(call.from_user.id, 'Ок, все записал 👌', reply_markup=Inline.result_inline)


@dp.callback_query_handler(lambda c: c.data == 'flex', state=Form.type_roof_)
async def flex(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['type_roof_'] = 2
    await bot.send_message(call.from_user.id, 'Ок, все записал 👌', reply_markup=Inline.result_inline)


@dp.callback_query_handler(lambda c: c.data == 'ceramic_roof', state=Form.type_roof_)
async def ceramic_roof(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['type_roof_'] = 3
    await bot.send_message(call.from_user.id, 'Ок, все записал 👌', reply_markup=Inline.result_inline)


@dp.callback_query_handler(lambda c: c.data == 'result', state=Form.type_roof_)
async def result(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.finish()
    square_ = int(data['square_'])
    number_floors = int(data['number_floors_'])
    type_foundation = int(data['type_found_'])
    material = int(data['material_'])
    roof_type = int(data['type_roof_'])
    summa = 0

    elements = square_ / 25

    if type_foundation == 1:  # Ленточный
        concrete_volume = elements * 5.2
        fittings = elements * 80
        summa_foundation = int(concrete_volume * 3000 + fittings * 50)
        summa += summa_foundation
    elif type_foundation == 2:  # Свайный
        concrete_volume = elements * 5.2
        fittings = elements * 80
        number_piles = int(elements * 12)
        summa_foundation = int(concrete_volume * 3000 + number_piles * 2000 + fittings * 50)
        summa += summa_foundation
    elif type_foundation == 3:  # Плитный
        concrete_volume = square_ * 0.3
        fittings = concrete_volume / 6.3 * 523
        summa_foundation = int(concrete_volume * 3000 + fittings * 50)
        summa += summa_foundation

    if material == 1:  # Брус
        bar_ = elements * 15 * number_floors
        summa_material = int(bar_ * 25000)
        summa += summa_material
    elif material == 2:  # Газобетонный блок
        aerated_concrete_block = elements * 400 * number_floors
        summa_material = int(aerated_concrete_block * 3000)
        summa += summa_material
    elif material == 3:  # Керамоблок
        ceramic_block = elements * 900 * number_floors
        summa_material = int(ceramic_block * 120)
        summa += summa_material
    elif material == 4:  # Кирпич
        brick_ = elements * 6000 * number_floors
        summa_material = int(brick_ * 19)
        summa += summa_material
    elif material == 5:  # Деревянный каркас
        racks = elements * 53 * number_floors
        summa_racks = int(racks * 110)
        overlap = elements * 20 * number_floors
        summa_overlap = int(overlap * 1000)
        summa_material = summa_racks + summa_overlap
        summa += summa_material

    if roof_type == 1:  # Листовые материалы
        sheet_material = elements * 37
        summa_roof = int(sheet_material * 500)
        summa += summa_roof
    elif roof_type == 2:  # Гибкая кровля
        flexible_roof = elements * 13
        summa_roof = int(flexible_roof * 500)
        summa += summa_roof
    elif roof_type == 3:  # Штучные материалы
        ceramic_roof_ = elements * 37
        summa_roof = int(ceramic_roof_ * 4000)
        summa += summa_roof
    print(summa_foundation, summa_material, summa_roof, summa)

    summa_foundation = str(summa_foundation)
    summa_foundation = summa_foundation[::-1]
    summa_foundation = '.'.join([summa_foundation[i:i + 3] for i in range(0, len(summa_foundation), 3)])
    summa_foundation = summa_foundation[::-1]

    summa_material = str(summa_material)
    summa_material = summa_material[::-1]
    summa_material = '.'.join([summa_material[i:i + 3] for i in range(0, len(summa_material), 3)])
    summa_material = summa_material[::-1]

    summa_roof = str(summa_roof)
    summa_roof = summa_roof[::-1]
    summa_roof = '.'.join([summa_roof[i:i + 3] for i in range(0, len(summa_roof), 3)])
    summa_roof = summa_roof[::-1]

    summa = str(summa)
    summa = summa[::-1]
    summa = '.'.join([summa[i:i + 3] for i in range(0, len(summa), 3)])
    summa = summa[::-1]

    text = 'Фундамент:  {0} р.\nСтеновой комплект:  {1} р.\nКровля:  {2} р.\n\nИтого:  {3} р.'.format(summa_foundation,
                                                                                                      summa_material,
                                                                                                      summa_roof,
                                                                                                      summa)
    await bot.send_message(call.from_user.id, text, reply_markup=Inline.restart_inline)
    await bot.send_message(1471718311, 'User {0} воспользовался конфигуратором\n{1}'.format(call.from_user.full_name,
                                                                                            text))


if __name__ == '__main__':
    executor.start_polling(dp)
