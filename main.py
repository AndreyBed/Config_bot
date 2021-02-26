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
    info_button = types.InlineKeyboardButton(text='Info', callback_data='info')
    start_inline.insert(start_button)
    start_inline.insert(info_button)

    restart_inline = types.InlineKeyboardMarkup()
    restart_button = types.InlineKeyboardButton(text='Рассчитать заново', callback_data='start')
    info_button = types.InlineKeyboardButton(text='Info', callback_data='info')
    restart_inline.insert(restart_button)
    restart_inline.insert(info_button)

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
    ceramic_block_button = types.InlineKeyboardButton(text='Керамоблок', callback_data='ceramic_block')
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

    info_inline = types.InlineKeyboardMarkup()
    found_button = types.InlineKeyboardButton(text='Фундамент', callback_data='info_found')
    material_button = types.InlineKeyboardButton(text='Стеновой комплект', callback_data='info_material')
    roof_button = types.InlineKeyboardButton(text='Кровля', callback_data='info_roof')
    info_inline.insert(found_button)
    info_inline.insert(roof_button)
    info_inline.add(material_button)

    info_found_inline = types.InlineKeyboardMarkup()
    info_tape_button = types.InlineKeyboardButton(text='Ленточный', callback_data='info_tape')
    info_pile_button = types.InlineKeyboardButton(text='Свайный', callback_data='info_pile')
    info_plate_button = types.InlineKeyboardButton(text='Плитный', callback_data='info_plate')
    info_found_inline.insert(info_tape_button)
    info_found_inline.insert(info_pile_button)
    info_found_inline.add(info_plate_button)

    info_material_inline = types.InlineKeyboardMarkup()
    info_bar_button = types.InlineKeyboardButton(text='Брус', callback_data='info_bar')
    info_aerated_concrete_block_button = types.InlineKeyboardButton(text='Газобетон', callback_data='info_ac_block')
    info_ceramic_block_button = types.InlineKeyboardButton(text='Керамоблок', callback_data='info_ceramic_block')
    info_brick_button = types.InlineKeyboardButton(text='Кирпич', callback_data='info_brick')
    info_door_button = types.InlineKeyboardButton(text='Деревянный каркас', callback_data='info_door')
    info_material_inline.insert(info_bar_button)
    info_material_inline.insert(info_ceramic_block_button)
    info_material_inline.add(info_aerated_concrete_block_button)
    info_material_inline.insert(info_brick_button)
    info_material_inline.add(info_door_button)

    info_roof_inline = types.InlineKeyboardMarkup()
    info_sheet_button = types.InlineKeyboardButton(text='Листовые материалы', callback_data='info_sheet')
    info_flexible_button = types.InlineKeyboardButton(text='Гибкая кровля', callback_data='info_flex')
    info_ceramic_roof_button = types.InlineKeyboardButton(text='Керамическая черепница',
                                                          callback_data='info_ceramic_roof')
    info_roof_inline.insert(info_sheet_button)
    info_roof_inline.add(info_flexible_button)
    info_roof_inline.add(info_ceramic_roof_button)


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


@dp.callback_query_handler(lambda c: c.data == 'info')
async def info(call: types.CallbackQuery):
    await bot.send_message(call.from_user.id, 'По какому разделу вопрос?', reply_markup=Inline.info_inline)


@dp.callback_query_handler(lambda c: c.data == 'info_found')
async def info_button(call: types.CallbackQuery):
    await bot.send_message(call.from_user.id, 'Выбери тип фундамента', reply_markup=Inline.info_found_inline)


@dp.callback_query_handler(lambda c: c.data == 'info_tape')
async def info_tape(call: types.CallbackQuery):
    photo = open('photos/tape.jpg', 'rb')
    await bot.send_message(call.from_user.id, 'Этот вид основания наиболее распространен в частном строительстве. '
                                              'Конструктивно ленточный фундамент представляет собой монолитную '
                                              'железобетонную конструкцию, идущую по всему периметру дома и под всеми '
                                              'несущими стенами. Часто заливается бетонное основание и под '
                                              'перегородками.')
    await bot.send_photo(call.from_user.id, photo, reply_markup=Inline.start_inline)


@dp.callback_query_handler(lambda c: c.data == 'info_pile')
async def imfo_pile(call: types.CallbackQuery):
    photo = open('photos/pile.jpg', 'rb')
    await bot.send_message(call.from_user.id, 'Самые популярные фундаменты в промышленном и многоэтажном жилом '
                                              'строительстве. Часто используются и при возведении небольших частных '
                                              'домов и коттеджей по современным технологиям. Если при строительстве '
                                              'промышленном способом на свайных фундаментах строят дома из любых '
                                              'материалов, то в частном секторе на сваях стоят преимущественно легкие '
                                              'сооружения из СИП-панелей, бруса, бревна.')
    await bot.send_photo(call.from_user.id, photo, reply_markup=Inline.start_inline)


@dp.callback_query_handler(lambda c: c.data == 'info_plate')
async def info_plate(call: types.CallbackQuery):
    photo = open('photos/plate.jpg', 'rb')
    await bot.send_message(call.from_user.id, 'Основания дома в виде сплошной или сборной плиты на всю площадь здания '
                                              'менее популярны, чем ленточные фундаменты, но в некоторых случаях '
                                              'являются единственно возможным вариантом. При строительстве на '
                                              'неустойчивых, песчано-глинистых, вспучивающихся грунтах, при высоком '
                                              'залегании грунтовых вод (выше 1 м), глубоко промерзающих почвах, лучше '
                                              'всего залить сплошную железобетонную плиту, на которой возводятся здания'
                                              ' любой этажности. Для каркасных одно и двухэтажных домов плитный '
                                              'фундамент практически идеальное решение. Он менее сложный, чем ленточный'
                                              ' и свайный, но по сравнению с ними более затратный в плане расхода '
                                              'материалов и требуемого количества рабочего времени.')
    await bot.send_photo(call.from_user.id, photo, reply_markup=Inline.start_inline)


@dp.callback_query_handler(lambda c: c.data == 'info_material')
async def info_material(call: types.CallbackQuery):
    await bot.send_message(call.from_user.id, 'Вот основные материалы стенового комплекта дома',
                           reply_markup=Inline.info_material_inline)


@dp.callback_query_handler(lambda c: c.data == 'info_bar')
async def info_bar(call: types.CallbackQuery):
    photo = open('photos/bar.jpg', 'rb')
    await bot.send_message(call.from_user.id, 'Именно брусу все чаще отдается предпочтение, что позволяет его назвать '
                                              'материалом № 1 в малоэтажном строительстве. Данная тенденция легко '
                                              'объяснима. Сравнивая плюсы и минусы дома из бруса, несложно прийти к '
                                              'заключению, что такие строения имеют ряд существенных преимуществ над '
                                              'коттеджами, дачами, особняками, выполненными из пенобетонных и прочих '
                                              'блоков, бревна, силикатного или обычного глиняного кирпича.')
    await bot.send_photo(call.from_user.id, photo, reply_markup=Inline.start_inline)


@dp.callback_query_handler(lambda c: c.data == 'info_ac_block')
async def info_ac_block(call: types.CallbackQuery):
    photo = open('photos/ac_block.jpg', 'rb')
    await bot.send_message(call.from_user.id, 'Газобетонные блоки применяются, прежде всего, для возведения наружных и '
                                              'внутренних стен жилых домов, магазинов, офисных зданий, ферм. Такую '
                                              'популярность рассматриваемый материал получил благодаря своим '
                                              'впечатляющим теплоизоляционным свойствам. Также к достоинствам '
                                              'газобетона относится высокая степень пожаробезопасности, относительно '
                                              'малый вес блоков и более легкий процесс укладки по сравнению с '
                                              'аналогичной процедурой по кирпичу.')
    await bot.send_photo(call.from_user.id, photo, reply_markup=Inline.start_inline)


@dp.callback_query_handler(lambda c: c.data == 'info_ceramic_block')
async def info_ceramic_block(call: types.CallbackQuery):
    photo = open('photos/ceramic_block.jpg', 'rb')
    await bot.send_message(call.from_user.id, 'Керамоблоки - это идеальный материал для возведения стен без '
                                              'дополнительных расходов на их теплоизоляцию. Сцепления «паз-гребень» '
                                              'скрепляют блоки без раствора, что даёт экономию на материалах и '
                                              'увеличивает скорость строительства. По сравнению с кирпичом раствора '
                                              'при укладке керамоблоков требуется меньше в 2-3 раза.')
    await bot.send_photo(call.from_user.id, photo, reply_markup=Inline.start_inline)


@dp.callback_query_handler(lambda c: c.data == 'info_brick')
async def info_brick(call: types.CallbackQuery):
    photo = open('photos/brick.jpg', 'rb')
    await bot.send_message(call.from_user.id, 'Кирпич сегодня – один из наиболее востребованных строительных материалов'
                                              ' для возведения зданий и сооружений: от небольших построек и заборов, до'
                                              ' высотных зданий и роскошных вилл. Кирпич – это искусственный камень '
                                              'геометрически правильной формы, полученный методом формовки и '
                                              'последующего обжига или обработки паром.')
    await bot.send_photo(call.from_user.id, photo, reply_markup=Inline.start_inline)


@dp.callback_query_handler(lambda c: c.data == 'info_door')
async def info_door(call: types.CallbackQuery):
    photo = open('photos/door.png', 'rb')
    await bot.send_message(call.from_user.id, 'Дома называются каркасными, потому что их основой является каркас из '
                                              'брусьев, который обшивается фанерой или OSB-плитами. В народе подобные '
                                              'сооружения получили название "засыпных" домов. Всё дело в использовании '
                                              'шлака, опилок или их смеси в качестве утеплителя в таких каркасных '
                                              'конструкциях.')
    await bot.send_photo(call.from_user.id, photo, reply_markup=Inline.start_inline)


@dp.callback_query_handler(lambda c: c.data == 'info_roof')
async def info_roof(call: types.CallbackQuery):
    await bot.send_message(call.from_user.id, 'Выбери материал кровли', reply_markup=Inline.info_roof_inline)


@dp.callback_query_handler(lambda c: c.data == 'info_sheet')
async def info_sheet(call: types.CallbackQuery):
    photo = open('photos/sheet.jfif', 'rb')
    await bot.send_message(call.from_user.id, 'Самый распространенный на сегодняшний день тип кровельного покрытия – '
                                              'это металлочерепица. Чем она заслужила такое признание? Ее отличает '
                                              'эстетичный внешний вид, прочность, надежность, а также достаточно '
                                              'простой монтаж. Металлические листы обладают высокой степенью '
                                              'устойчивости к коррозии, воздействию осадков и солнечных лучей.')
    await bot.send_photo(call.from_user.id, photo, reply_markup=Inline.start_inline)


@dp.callback_query_handler(lambda c: c.data == 'info_flex')
async def info_flex(call: types.CallbackQuery):
    photo = open('photos/flex.jpg', 'rb')
    await bot.send_message(call.from_user.id, 'У гибкой черепицы много названий: мягкая кровля, битумная черепица, '
                                              'кровельная плитка, шинглас, гонт. Все это плоские листы-модули '
                                              'небольшого размера с фигурным вырезом по одному краю, которые укладывают'
                                              ' внахлест. Их выпускают во всем многообразии форм и цветовых решений. '
                                              'Гибкую кровлю применяют на крышах с уклоном от 12° — как при укладке '
                                              'новой кровли, так и при реконструкции устаревших кровельных покрытий. '
                                              'Мягкая черепица подходит для частных коттеджей, зданий общественного '
                                              'пользования, коммерческих построек, промышленных сооружений, особенно в '
                                              'тех случаях, когда крыша имеет сложную форму.')
    await bot.send_photo(call.from_user.id, photo, reply_markup=Inline.start_inline)


@dp.callback_query_handler(lambda c: c.data == 'info_ceramic_roof')
async def info_ceramic_roof(call: types.CallbackQuery):
    photo = open('photos/ceramic_roof.jpg', 'rb')
    await bot.send_message(call.from_user.id, 'Керамическая черепица – одна из самых древних материалов для покрытия '
                                              'крыши. Её история насчитывает несколько тысячелетий, и даже сегодня она '
                                              'считается модным и даже успела стать элитным покрытием. Такая '
                                              'популярность легко объяснима: керамическая кровля не только прекрасно '
                                              'смотрится – она ещё и долговечна, водонепроницаема, огнестойка и на все '
                                              '100% является экологически чистой.')
    await bot.send_photo(call.from_user.id, photo, reply_markup=Inline.start_inline)


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
