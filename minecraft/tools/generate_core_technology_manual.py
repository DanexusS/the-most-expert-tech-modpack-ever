from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAPTER_DIR = ROOT / "config" / "ftbquests" / "quests" / "chapters"
LANG_DIR = ROOT / "config" / "ftbquests" / "quests" / "lang"
CHAPTER_PATH = CHAPTER_DIR / "core_technology_manual_1.snbt"

MODULES = [
    {
        "slug": "create",
        "title_en": "Create: Kinetic Engineering",
        "title_ru": "Create: кинетическая инженерия",
        "icon": "create:large_cogwheel",
        "lessons": [
            ("network_model", "create:shaft", "Rotational Network Model", "Модель вращательной сети",
             ["Create transmits rotation through connected components. Speed, direction and stress capacity are separate properties and must be inspected together.", "A working design starts with a labelled source, a measurable distribution path and an intentional shutdown point; adding shafts does not add capacity."],
             ["Create передаёт вращение через соединённые компоненты. Скорость, направление и запас нагрузки являются разными свойствами и проверяются вместе.", "Рабочая схема начинается с подписанного источника, измеримого пути распределения и предусмотренной остановки; дополнительные валы не увеличивают мощность."]),
            ("sources", "create:water_wheel", "Sources and Stress Capacity", "Источники и запас нагрузки",
             ["Water wheels, steam engines and other sources provide stress capacity. Consumers spend that capacity according to their stress impact and current speed.", "Keep normal operation below the absolute limit, reserve capacity for startup spikes and split independent factories instead of building one fragile universal shaft."],
             ["Водяные колёса, паровые двигатели и другие источники создают запас нагрузки. Потребители расходуют его с учётом своего влияния и текущей скорости.", "Обычная работа должна оставаться ниже предела; оставляйте резерв на запуск и разделяйте независимые фабрики вместо одного хрупкого общего вала."]),
            ("ratios", "create:large_cogwheel", "Ratios, Speed and Direction", "Передаточные отношения, скорость и направление",
             ["Cogwheel ratios and speed controllers change RPM, while gearboxes and chain drives route direction. Faster processing usually increases stress demand.", "Choose speed from the slowest stable process, document every ratio change and avoid hidden direction reversals that only appear after a line is expanded."],
             ["Передаточные отношения шестерён и контроллеры меняют обороты, а коробки и цепные передачи направляют вращение. Ускорение обычно повышает нагрузку.", "Выбирайте скорость по самому медленному устойчивому процессу, отмечайте каждое изменение отношения и не скрывайте развороты направления внутри разросшейся линии."]),
            ("belts", "create:belt_connector", "Belts and Visible Throughput", "Ремни и видимая пропускная способность",
             ["Belts make item flow observable, which is useful for finding spacing problems, blocked outputs and uneven processing times.", "A belt line needs controlled insertion, extraction, overflow handling and enough spacing for the slowest machine; visual motion is not proof of sustained throughput."],
             ["Ремни делают поток предметов видимым и помогают находить неверные интервалы, заполненные выходы и разное время операций.", "Линия требует управляемой загрузки, выгрузки, обработки переполнения и расстояния под самую медленную машину; движение предметов ещё не доказывает устойчивую производительность."]),
            ("processing", "create:mechanical_press", "Mechanical Processing Cells", "Механические производственные ячейки",
             ["Presses, mixers, crushers, saws and deployers should be arranged as repeatable cells with defined inputs, outputs and recovery access.", "Test each cell with a full batch, return reusable tools and containers, and stop upstream delivery before a full destination scatters or destroys workpieces."],
             ["Прессы, смесители, дробители, пилы и манипуляторы следует оформлять повторяемыми ячейками с определёнными входами, выходами и доступом для восстановления.", "Проверяйте полную партию, возвращайте инструменты и контейнеры, останавливайте верхнюю подачу до того, как заполненный выход потеряет заготовки."]),
            ("sequenced", "create:precision_mechanism", "Sequenced Assembly", "Последовательная сборка",
             ["Sequenced assembly applies several operations to an incomplete item. Wrong order, missing tools or uncontrolled recirculation can consume materials without producing a result.", "Use a bounded loop, verify every operation and chance, recover incomplete items and maintain enough component stock for one complete sequence rather than one individual step."],
             ["Последовательная сборка применяет несколько операций к незавершённому предмету. Неверный порядок, отсутствующий инструмент или бесконтрольная циркуляция расходуют материалы без результата.", "Используйте ограниченный цикл, проверяйте операции и вероятность, возвращайте незавершённые детали и храните запас на полный маршрут, а не на один шаг."]),
            ("fluids", "create:mechanical_pump", "Fluid Networks", "Жидкостные сети",
             ["Pumps define flow direction and tanks provide buffering. Pipe connectivity alone does not guarantee correct routing when several fluids or consumers share a network.", "Separate incompatible fluids, label pump direction, reserve expansion capacity and ensure a full output tank stops production before the source is wasted."],
             ["Насосы задают направление, а баки создают буфер. Одного соединения труб недостаточно, когда сеть обслуживает несколько жидкостей или потребителей.", "Разделяйте несовместимые жидкости, отмечайте направление насосов, оставляйте резерв и останавливайте производство при заполнении выхода до потери сырья."]),
            ("filters", "create:brass_funnel", "Filters and Stock Control", "Фильтры и контроль запасов",
             ["Funnels, tunnels, filters and threshold switches turn visible transport into controlled logistics. Broad filters are convenient but can route future items into the wrong machine.", "Use explicit tags only when their membership is intended, cap maintained stock and test the line with an unexpected item before trusting unattended production."],
             ["Воронки, тоннели, фильтры и пороговые переключатели превращают транспорт в управляемую логистику. Слишком широкие фильтры отправляют новые предметы не в те машины.", "Используйте теги только при осознанном составе, ограничивайте поддерживаемый запас и проверяйте линию неожиданным предметом до автономной работы."]),
            ("contraptions", "create:mechanical_piston", "Contraptions and Moving Inventories", "Механизмы и движущиеся инвентари",
             ["Contraptions move blocks, inventories and tools as one assembly. Movement changes which interfaces remain accessible and how items are transferred at stations.", "Provide safe clearance, emergency disassembly, predictable loading and unloading, and a recovery plan for a stopped assembly outside its home position."],
             ["Механизмы перемещают блоки, инвентари и инструменты как единую конструкцию. Движение меняет доступность интерфейсов и передачу предметов на станциях.", "Обеспечьте свободное пространство, аварийную разборку, предсказуемую загрузку и план возврата остановившейся конструкции вне домашней позиции."]),
            ("trains", "create:track", "Rail Logistics", "Железнодорожная логистика",
             ["Trains are long-distance logistics systems, not faster belts. Schedules, station ownership, chunk availability and transfer time determine reliability.", "Separate passenger and freight intent, prevent two stations from competing for one cargo, include timeout behavior and keep critical recovery supplies on both sides of a route."],
             ["Поезда являются системой дальней логистики, а не ускоренным ремнём. Надёжность определяют расписания, станции, загрузка чанков и время передачи.", "Разделяйте пассажирские и грузовые задачи, не допускайте конкуренции станций за один груз, задавайте поведение при ожидании и храните аварийные запасы с обеих сторон."]),
            ("diagnostics", "create:goggles", "Create Diagnostics", "Диагностика Create",
             ["Goggles and network readouts reveal stress, speed and machine state. Diagnose from the first failed boundary instead of replacing random shafts or adding uncontrolled power.", "Record source capacity, consumer load, RPM and blocked inventory state; reproduce the failure with a small batch before changing a working production network."],
             ["Очки и показания сети раскрывают нагрузку, скорость и состояние машин. Ищите первую нарушенную границу вместо случайной замены валов и бесконтрольного добавления мощности.", "Записывайте мощность источника, нагрузку, обороты и заполнение инвентарей; воспроизводите сбой малой партией до изменения рабочей сети."]),
            ("project", "kubejs:kinetic_interface", "Project: Repeatable Kinetic Factory", "Проект: повторяемая кинетическая фабрика",
             ["Build one factory that accepts buffered raw materials and produces at least three processed outputs through separate, measurable cells.", "The project passes when it restarts after empty inputs, stops safely on full outputs, shows stress reserve, exposes bottlenecks and completes two consecutive batches without manual item movement."],
             ["Постройте фабрику, принимающую буферизованное сырьё и выпускающую минимум три продукта через отдельные измеримые ячейки.", "Проект принят, когда линия перезапускается после нехватки, безопасно останавливается при заполнении, показывает резерв нагрузки и выполняет две партии без ручного переноса предметов."]),
        ],
    },
    {
        "slug": "ie",
        "title_en": "Immersive Engineering: Industrial Systems",
        "title_ru": "Immersive Engineering: промышленные системы",
        "icon": "immersiveengineering:hammer",
        "lessons": [
            ("manual", "immersiveengineering:manual", "Engineer's Manual and Multiblocks", "Руководство инженера и мультиблоки",
             ["Immersive Engineering uses shaped multiblocks with specific orientation, formation points and input/output faces. The manual is part of the machine interface, not optional flavor text.", "Before forming a structure, verify dimensions, clear maintenance space and label planned ports so later pipes and wires do not block access."],
             ["Immersive Engineering использует ориентированные мультиблоки с точками формирования и определёнными гранями. Руководство является частью интерфейса машин, а не декоративным текстом.", "До формирования проверьте размеры, оставьте обслуживание и подпишите порты, чтобы будущие трубы и провода не перекрыли доступ."]),
            ("coke", "immersiveengineering:cokebrick", "Coke Oven and Creosote", "Коксовая печь и креозот",
             ["The Coke Oven produces both solid coke products and creosote. Either full output can halt the same process.", "Provide independent storage, convert creosote into planned treated-wood batches and preserve enough coke for steel production instead of consuming every output as fuel."],
             ["Коксовая печь выпускает твёрдый кокс и креозот. Заполнение любого выхода останавливает один и тот же процесс.", "Создайте независимые хранилища, планируйте партии обработанной древесины и сохраняйте кокс для стали вместо полного расходования как топлива."]),
            ("steel", "immersiveengineering:blastbrick_reinforced", "Steel Production", "Производство стали",
             ["Blast furnaces convert iron and coke into steel with slag as a secondary output. Preheaters improve throughput but add continuous power demand.", "Balance coke supply, iron input, slag extraction and output storage; measure the complete batch time before deciding whether another furnace or preheater is justified."],
             ["Доменные печи превращают железо и кокс в сталь с побочным шлаком. Подогреватели ускоряют процесс, но требуют постоянной энергии.", "Согласуйте кокс, железо, удаление шлака и хранение стали; измерьте полную партию до решения о второй печи или подогревателе."]),
            ("wires", "immersiveengineering:wirecoil_copper", "Wire Tiers and Loss Boundaries", "Уровни проводов и границы потерь",
             ["Wire types differ in transfer limits and intended voltage tier. A connector, relay or machine can become the bottleneck even when the generator is large enough.", "Document each tier transition, avoid accidental long-distance low-tier trunks and protect critical machines from sharing a line with irregular high-demand consumers."],
             ["Типы проводов отличаются пределом передачи и уровнем напряжения. Ограничением становится соединитель, реле или машина даже при достаточном генераторе.", "Документируйте переходы уровней, избегайте длинных слабых магистралей и не объединяйте критические машины с нерегулярными мощными потребителями."]),
            ("connectors", "immersiveengineering:connector_lv", "Connectors, Relays and Topology", "Соединители, реле и топология",
             ["Connectors terminate energy at machines; relays route wires without exposing an inventory or power port. Mixing their roles creates confusing networks.", "Build a readable topology with junction labels, service isolation and no crossing wire that must be removed to reach another component."],
             ["Соединители завершают линию на машине, а реле направляют провод без собственного порта. Смешение ролей делает сеть неясной.", "Стройте читаемую топологию с подписями узлов, изоляцией обслуживания и без проводов, которые приходится снимать ради доступа к другому компоненту."]),
            ("capacitors", "immersiveengineering:capacitor_lv", "Buffers and Demand Spikes", "Буферы и скачки нагрузки",
             ["Capacitors separate generation rate from short demand spikes and expose whether a network is slowly losing energy over time.", "Size buffers from measured cycle demand, configure input/output sides deliberately and test recovery after simultaneous machine startup rather than relying on a full idle capacitor."],
             ["Конденсаторы отделяют скорость генерации от кратких пиков и показывают, теряет ли сеть энергию со временем.", "Размер выбирайте по измеренному циклу, явно задавайте стороны и проверяйте восстановление после одновременного запуска, а не по заполненному в простое буферу."]),
            ("components", "immersiveengineering:component_steel", "Standard Components", "Стандартные компоненты",
             ["Iron, steel and electronic components recur across tools and multiblocks. Producing them one at a time turns every later machine into a manual interruption.", "Maintain minimum stock, record component demand by project and automate plates, rods and wires before expanding into machines that consume them continuously."],
             ["Железные, стальные и электронные компоненты повторяются в инструментах и мультиблоках. Поодиночный выпуск превращает каждую машину в ручное прерывание.", "Поддерживайте минимальный запас, учитывайте расход по проектам и автоматизируйте пластины, стержни и провода до непрерывно потребляющих машин."]),
            ("fluids", "immersiveengineering:fluid_pump", "Pumps, Pipes and Tank Safety", "Насосы, трубы и безопасность баков",
             ["Fluid pipes share capacity and pumps define active movement. A visually connected line may still fail because a side, redstone mode or destination is incorrect.", "Label fluids, separate incompatible networks, expose tank levels and stop producers before a full destination forces a valuable byproduct to block the plant."],
             ["Трубы делят пропускную способность, а насосы задают активное движение. Внешне соединённая линия не работает при неверной стороне, режиме сигнала или назначении.", "Подписывайте жидкости, разделяйте сети, показывайте уровни и останавливайте производство до того, как полный бак заблокирует ценный побочный продукт."]),
            ("diesel", "immersiveengineering:diesel_generator", "Fuel Processing and Diesel Generation", "Переработка топлива и дизельная генерация",
             ["Diesel generation depends on an entire chain of crops or oil products, refining, fluid buffers and generator demand; the generator alone is not the system.", "Calculate net energy after farm and processing costs, reserve startup fuel and prevent a power failure from disabling the pumps needed to restore fuel production."],
             ["Дизельная генерация зависит от цепочки сырья, переработки, буферов и спроса; один генератор не является системой.", "Рассчитайте чистую энергию после затрат фермы и переработки, храните стартовое топливо и не допускайте отключения насосов, нужных для восстановления производства."]),
            ("excavator", "immersiveengineering:excavator", "Excavator Project Planning", "Планирование экскаватора",
             ["The Excavator is a large regional extraction project with high continuous energy demand and deposit-dependent output.", "Survey before construction, provide bulk transport and overflow, compare deposit value with operating cost and ensure the machine cannot become an early source of progression-locked materials."],
             ["Экскаватор является крупным региональным проектом с высоким постоянным спросом и выходом, зависящим от месторождения.", "Проводите разведку до строительства, обеспечьте массовый транспорт, сравните ценность залежи с затратами и исключите раннюю добычу закрытых материалов."]),
            ("diagnostics", "immersiveengineering:voltmeter", "Industrial Diagnostics", "Промышленная диагностика",
             ["The voltmeter and visible machine state should be used to locate the first failing boundary: generation, wire capacity, machine input, fluid supply or blocked output.", "Record measurements before changing the network, isolate one section at a time and preserve a known-good baseline so an attempted repair does not create a second fault."],
             ["Вольтметр и состояние машин помогают найти первую нарушенную границу: генерацию, провод, вход, жидкость или заполненный выход.", "Записывайте измерения, изолируйте по одному участку и сохраняйте рабочую базовую схему, чтобы попытка ремонта не создала вторую неисправность."]),
            ("project", "kubejs:structural_lattice", "Project: Integrated Industrial Yard", "Проект: единый промышленный двор",
             ["Construct a serviceable yard that produces coke, creosote products and steel while feeding one powered IE machine through a documented wire network.", "The project passes when all byproducts are handled, buffers expose shortages, maintenance access remains open and two complete steel batches finish without manual transfers."],
             ["Постройте обслуживаемый двор, выпускающий кокс, продукты креозота и сталь, и питающий одну машину IE через документированную сеть.", "Проект принят, когда побочные продукты обработаны, дефициты видны, доступ открыт и две партии стали проходят без ручных переносов."]),
        ],
    },
    {
        "slug": "mi",
        "title_en": "Modern Industrialization: Factory Engineering",
        "title_ru": "Modern Industrialization: фабричная инженерия",
        "icon": "modern_industrialization:motor",
        "lessons": [
            ("steam", "modern_industrialization:bronze_boiler", "Steam as a Production Utility", "Пар как производственная среда",
             ["Early MI machines are a shared steam system. Boiler fuel, water delivery, steam storage and pipe throughput determine whether individual machines can sustain work.", "Keep dry-boiler protection, reserve water, separate generation from consumers and measure steam recovery between batches."],
             ["Ранние машины MI используют общую паровую систему. Топливо, вода, хранение пара и трубы определяют устойчивость работы.", "Защитите котёл от работы без воды, храните резерв, отделяйте генерацию от потребителей и измеряйте восстановление пара между партиями."]),
            ("bronze", "modern_industrialization:bronze_macerator", "Bronze Machine Workshop", "Бронзовая машинная мастерская",
             ["Bronze machines establish crushing, smelting, cutting and compression before electrical tiers. Their low speed is intended to teach flow design, not permanent manual feeding.", "Build common input and output buffers, preserve byproducts and queue enough work to observe the actual slowest machine."],
             ["Бронзовые машины создают дробление, плавку, резку и прессование до электрических уровней. Низкая скорость учит проектированию потока, а не вечной ручной подаче.", "Создайте общие буферы, сохраняйте побочные продукты и запускайте партию, достаточную для определения самого медленного узла."]),
            ("pipes", "modern_industrialization:bronze_item_pipe", "Item and Fluid Pipe Contracts", "Контракты предметных и жидкостных труб",
             ["MI pipes use connections, extraction settings and filters to define movement. A pipe touching a machine is not automatically a valid route.", "Document extraction points, avoid circular routes, reserve maintenance sides and test the network with a blocked destination and an unexpected item."],
             ["Трубы MI используют соединения, извлечение и фильтры. Касание машины ещё не создаёт правильный маршрут.", "Документируйте точки извлечения, избегайте циклов, оставляйте стороны обслуживания и проверяйте сеть при заполненном выходе и неожиданном предмете."]),
            ("electricity", "modern_industrialization:basic_machine_hull", "Electric Tier Transition", "Переход к электрическому уровню",
             ["Electric hulls replace steam consumption with voltage-tiered energy and recurring circuits, motors and cables.", "Move only after component stock and generation can support several machines; one powered hull without a component supply chain is not an industrial transition."],
             ["Электрические корпуса заменяют пар уровнями напряжения и постоянным расходом схем, моторов и кабелей.", "Переходите после подготовки запаса компонентов и генерации для нескольких машин; один корпус без цепочки снабжения не является индустриализацией."]),
            ("voltage", "modern_industrialization:lv_transformer", "Voltage and Transformer Boundaries", "Напряжение и границы трансформаторов",
             ["Machine tiers accept specific voltage classes. Transformers connect tiers but do not make an undersized cable or generator safe.", "Label every boundary, isolate new machines during commissioning and verify both normal draw and startup behavior before joining a production bus."],
             ["Машины принимают определённые классы напряжения. Трансформатор соединяет уровни, но не исправляет слабый кабель или генератор.", "Подписывайте границы, изолируйте новые машины при вводе и проверяйте обычное и пусковое потребление до подключения к магистрали."]),
            ("overclock", "modern_industrialization:overdrive_module", "Overclocking and Energy Cost", "Разгон и стоимость энергии",
             ["Overclocking improves throughput by increasing machine energy demand and may shift the bottleneck into generation, input transport or output handling.", "Add upgrades only after measuring a complete line, preserve thermal and power margin and compare parallel machines with one heavily upgraded machine."],
             ["Разгон повышает выпуск ценой энергии и переносит узкое место в генерацию, подачу или выгрузку.", "Добавляйте улучшения после измерения всей линии, сохраняйте запас и сравнивайте параллельные машины с одной сильно ускоренной."]),
            ("circuits", "modern_industrialization:electronic_circuit", "Circuit Production", "Производство схем",
             ["Circuits are tier gates assembled from plates, wires, components and increasingly complex intermediate parts.", "Stock recurring subcomponents, separate circuit tiers, record per-machine demand and avoid consuming the last lower-tier circuit needed to rebuild its own production line."],
             ["Схемы являются допусками уровней и собираются из пластин, проводов и усложняющихся промежуточных деталей.", "Храните повторяющиеся компоненты, разделяйте уровни, учитывайте расход и не тратьте последнюю младшую схему, необходимую для восстановления её производства."]),
            ("multiblocks", "modern_industrialization:large_steam_boiler", "Industrial Multiblocks", "Промышленные мультиблоки",
             ["Large MI structures trade construction and infrastructure cost for sustained throughput. Hatch placement and tier compatibility define the actual machine.", "Plan ports before building, leave service corridors, match energy and fluid hatches and verify minimum and expanded forms separately."],
             ["Крупные структуры MI обменивают стоимость строительства на устойчивый выпуск. Размещение люков и совместимость уровней определяют машину.", "Планируйте порты заранее, оставляйте коридоры, согласуйте энергетические и жидкостные люки и отдельно проверяйте минимальную и расширенную форму."]),
            ("byproducts", "modern_industrialization:chemical_reactor", "Byproducts and Closed Loops", "Побочные продукты и замкнутые циклы",
             ["Chemical and refining recipes often return secondary fluids or materials that are required elsewhere. Voiding them can make a later chain unnecessarily expensive.", "Map every output, recycle only when the loop has a controlled purge and ensure a full low-value byproduct cannot stop a high-value process."],
             ["Химические и перерабатывающие рецепты часто возвращают вторичные жидкости и материалы для других цепочек. Сброс делает поздние процессы неоправданно дорогими.", "Картируйте выходы, замыкайте цикл только с управляемым сбросом и не позволяйте дешёвому побочному продукту остановить ценный процесс."]),
            ("assembler", "modern_industrialization:assembler", "Assembler and Repeated Components", "Сборщик и повторяющиеся компоненты",
             ["The Assembler converts component stocking into repeatable machine production. It becomes useful only when inputs arrive in stable ratios and outputs leave automatically.", "Run several recipes, isolate incompatible fluids, keep templates documented and verify the line can rebuild one of its own upstream components."],
             ["Сборщик превращает запасы компонентов в повторяемое производство машин. Он полезен только при стабильных соотношениях входов и автоматическом выходе.", "Запустите несколько рецептов, разделите жидкости, документируйте шаблоны и проверьте способность линии восстановить один из собственных верхних компонентов."]),
            ("diagnostics", "modern_industrialization:wrench", "MI Diagnostics and Maintenance", "Диагностика и обслуживание MI",
             ["A stopped MI line should be diagnosed by energy tier, pipe extraction, recipe inputs, machine progress and output capacity in that order.", "Preserve wrench access, label side configuration, use test batches and compare expected material balance with actual inventories before replacing machines."],
             ["Остановившуюся линию MI проверяйте по порядку: уровень энергии, извлечение труб, входы рецепта, прогресс и ёмкость выхода.", "Сохраняйте доступ ключом, подписывайте стороны, используйте тестовые партии и сравнивайте расчётный баланс с фактическими запасами до замены машин."]),
            ("project", "modern_industrialization:assembler", "Project: Steam-to-Electric Factory", "Проект: фабрика от пара к электричеству",
             ["Build a factory that turns raw ore into processed material, manufactures recurring components and assembles one electric machine without hand-moving intermediate items.", "The project passes after two repeated builds, safe recovery from a full output, documented voltage boundaries and a stored reserve of every component required to restart production."],
             ["Постройте фабрику, перерабатывающую руду, выпускающую повторяющиеся компоненты и собирающую электрическую машину без ручного переноса промежуточных предметов.", "Проект принят после двух повторов, восстановления после полного выхода, документированных напряжений и резерва компонентов для перезапуска."]),
        ],
    },
    {
        "slug": "ae2",
        "title_en": "Applied Energistics 2: Network Architecture",
        "title_ru": "Applied Energistics 2: архитектура сети",
        "icon": "ae2:controller",
        "lessons": [
            ("quartz", "ae2:certus_quartz_crystal", "Certus, Fluix and Crystal Supply", "Цертус, флюикс и снабжение кристаллами",
             ["AE2 depends on recurring certus, charged certus and fluix products. Treat them as production materials rather than one-time quest items.", "Automate charging and fluix preparation, separate crystal states and keep enough reserve to rebuild power, terminals and processor production after a network failure."],
             ["AE2 постоянно использует цертус, заряженный цертус и флюикс. Это производственные материалы, а не одноразовые предметы задания.", "Автоматизируйте зарядку и флюикс, разделяйте состояния и храните резерв для восстановления питания, терминалов и процессоров после отказа."]),
            ("power", "ae2:energy_acceptor", "Network Power and Idle Cost", "Питание сети и расход простоя",
             ["Every active device contributes to AE network demand. A system can fail during autocrafting even when idle power appears stable.", "Use external buffering, observe idle and peak draw, isolate nonessential devices and ensure power loss does not trap the only tools needed to repair the network."],
             ["Каждое активное устройство добавляет потребление сети. Система отключается во время автокрафта, даже если в простое выглядит стабильной.", "Используйте внешний буфер, измеряйте простой и пик, изолируйте второстепенные устройства и не храните единственные инструменты ремонта только внутри сети."]),
            ("channels", "ae2:smart_cable", "Channels and Dense Trunks", "Каналы и плотные магистрали",
             ["Channels are a topology constraint. Smart cables expose usage, dense cables aggregate branches and ad-hoc expansion can silently exceed a path limit.", "Budget channels before placement, label trunks, reserve expansion and design failure boundaries so one cut does not remove storage, crafting and monitoring together."],
             ["Каналы являются ограничением топологии. Умные кабели показывают использование, плотные объединяют ветви, а случайное расширение незаметно превышает предел.", "Планируйте каналы, подписывайте магистрали, оставляйте резерв и разделяйте отказ так, чтобы один разрыв не отключал хранение, крафт и мониторинг."]),
            ("cells", "ae2:item_storage_cell_16k", "Cells, Bytes and Types", "Ячейки, байты и типы",
             ["Storage cells have both byte capacity and type limits. Many tiny stacks can fill types while leaving most bytes unused.", "Separate bulk materials from diverse equipment, partition specialized cells, expose remaining capacity and provide an overflow route that cannot loop back into the same full storage."],
             ["Ячейки имеют предел байтов и типов. Множество малых стаков заполняет типы при свободных байтах.", "Разделяйте массовые материалы и разнообразное снаряжение, размечайте специальные ячейки, показывайте остаток и выводите переполнение без возврата в то же заполненное хранилище."]),
            ("external", "ae2:storage_bus", "External Storage and Priority", "Внешнее хранение и приоритет",
             ["Storage buses expose external inventories to the network. Priorities decide insertion and extraction order, while duplicate exposure can create recursive behavior.", "Connect an inventory once, document priority, reserve machine output space and test extraction after both preferred and fallback stores contain the same item."],
             ["Шины хранения открывают внешние инвентари. Приоритет определяет порядок, а двойное подключение создаёт рекурсивное поведение.", "Подключайте инвентарь один раз, документируйте приоритет, оставляйте место выходу машин и проверяйте извлечение при наличии предмета в основном и резервном хранилище."]),
            ("subnets", "ae2:quartz_fiber", "Subnets and Functional Boundaries", "Подсети и функциональные границы",
             ["Subnets isolate channels and functions while quartz fiber can share power without joining channel logic.", "Create dedicated import, storage or machine-control subnets, document their boundary and verify the main network remains usable when one subnet is disconnected."],
             ["Подсети изолируют каналы и функции, а кварцевое волокно передаёт питание без объединения логики каналов.", "Создавайте отдельные подсети импорта, хранения или управления, документируйте границу и проверяйте работу основной сети при отключении одной подсети."]),
            ("processors", "ae2:engineering_processor", "Processor Manufacturing", "Производство процессоров",
             ["Logic, calculation and engineering processors are recurring parts. Manual press swapping creates mistakes and blocks all advanced infrastructure.", "Dedicate or positively route presses, automate silicon and printed parts, return reusable tools and keep a minimum stock for emergency network reconstruction."],
             ["Логические, вычислительные и инженерные процессоры постоянно расходуются. Ручная смена прессов создаёт ошибки и блокирует инфраструктуру.", "Выделяйте высекатели или надёжно маршрутизируйте прессы, автоматизируйте кремний и печатные детали, возвращайте инструменты и храните аварийный запас."]),
            ("patterns", "ae2:pattern_provider", "Processing and Crafting Patterns", "Шаблоны обработки и крафта",
             ["Crafting patterns describe grid recipes; processing patterns describe an external transformation. Using the wrong type hides outputs or creates loops.", "Name providers by destination, encode every secondary output, prevent recipes that request their own output and test one pattern with unavailable input before enabling bulk requests."],
             ["Шаблоны крафта описывают сетку, а обработки — внешнее преобразование. Неверный тип скрывает выходы или создаёт цикл.", "Подписывайте провайдеры по назначению, указывайте побочные выходы, исключайте запрос собственного результата и проверяйте шаблон при отсутствующем входе до массовых заказов."]),
            ("cpu", "ae2:crafting_unit", "Crafting CPU Capacity", "Ёмкость процессора крафта",
             ["Crafting storage limits the size of an active job and co-processors allow more parallel processing steps; neither fixes a missing ingredient or blocked machine.", "Size CPUs from measured jobs, separate critical and bulk requests, expose stuck tasks and keep one small CPU free for recovery components during a large craft."],
             ["Хранилище крафта ограничивает размер задания, а сопроцессоры добавляют параллельные операции; они не исправляют отсутствующий вход или заполненную машину.", "Выбирайте размер по измеренным заказам, разделяйте критические и массовые задачи, показывайте зависания и оставляйте малый процессор для аварийных компонентов."]),
            ("p2p", "ae2:me_p2p_tunnel", "P2P Tunnels", "P2P-туннели",
             ["P2P tunnels transport channels or other resources through an AE path. They compress topology but make undocumented networks difficult to repair.", "Label input/output pairs, avoid hidden nested dependencies, reserve tunnel capacity and verify endpoint loss fails only the intended subsystem."],
             ["P2P-туннели передают каналы или другие ресурсы через сеть AE. Они уплотняют топологию, но усложняют ремонт без документации.", "Подписывайте пары входа и выхода, избегайте скрытых вложенных зависимостей, оставляйте резерв и проверяйте, что потеря точки отключает только нужную подсистему."]),
            ("quantum", "ae2:quantum_ring", "Quantum Network Link", "Квантовая связь сети",
             ["Quantum bridges connect distant networks with substantial ongoing energy demand and two critical endpoints.", "Power both sides independently, keep recovery items outside the bridge, test reconnection and ensure unloaded or failed remote infrastructure cannot stall unrelated local autocrafting."],
             ["Квантовый мост соединяет удалённые сети с высоким постоянным потреблением и двумя критическими точками.", "Питайте стороны независимо, храните аварийные предметы вне моста, проверяйте восстановление и не позволяйте удалённому отказу остановить местный автокрафт."]),
            ("project", "kubejs:quantum_logic", "Project: Resilient Autocrafting Network", "Проект: отказоустойчивая сеть автокрафта",
             ["Build a channel-documented network with bulk and diverse storage, one functional subnet, automated processors and at least five external processing patterns.", "The project passes when two simultaneous jobs finish, one subnet can be disconnected safely, a blocked machine is diagnosable and recovery parts remain available during a large request."],
             ["Постройте сеть с документированными каналами, раздельным хранением, функциональной подсетью, автоматическими процессорами и минимум пятью внешними шаблонами.", "Проект принят, когда два заказа завершаются, подсеть безопасно отключается, заполненная машина диагностируется, а детали восстановления доступны во время крупного запроса."]),
        ],
    },
    {
        "slug": "mekanism",
        "title_en": "Mekanism: Chemical Industry",
        "title_ru": "Mekanism: химическая промышленность",
        "icon": "mekanism:ultimate_control_circuit",
        "lessons": [
            ("tiers", "mekanism:basic_control_circuit", "Circuits, Alloys and Machine Tiers", "Схемы, сплавы и уровни машин",
             ["Mekanism tiers consume recurring control circuits and infused alloys. Building only the final machine hides a component bottleneck.", "Automate infusion inputs, stock every lower tier and reserve enough components to rebuild the machine that produces the next tier."],
             ["Уровни Mekanism постоянно расходуют управляющие схемы и инфузионные сплавы. Сборка только конечной машины скрывает узкое место компонентов.", "Автоматизируйте инфузию, храните каждый младший уровень и оставляйте запас для восстановления машины, производящей следующий уровень."]),
            ("upgrades", "mekanism:upgrade_speed", "Upgrades, Factories and Energy", "Улучшения, фабрики и энергия",
             ["Speed and factory upgrades increase parallel throughput and energy demand. Energy upgrades reduce cost but do not solve input or output saturation.", "Upgrade after measuring the complete line, size cables and buffers for peak draw and compare one factory with several independently serviceable machines."],
             ["Ускорение и фабрики повышают параллельный выпуск и потребление. Энергоулучшения снижают расход, но не исправляют переполнение входов и выходов.", "Улучшайте после измерения линии, рассчитывайте кабели и буферы на пик и сравнивайте фабрику с несколькими обслуживаемыми машинами."]),
            ("transport", "mekanism:ultimate_logistical_transporter", "Transporters and Side Configuration", "Транспортёры и настройка сторон",
             ["Items, fluids, gases and energy use different transport systems with pull/push rules, color channels and machine side configuration.", "Label each medium, avoid unrestricted round trips, preserve maintenance sides and test the network with a full destination and a disabled consumer."],
             ["Предметы, жидкости, газы и энергия используют разные транспортные системы с режимами, цветами и сторонами машин.", "Подписывайте среды, исключайте бесконтрольные циклы, сохраняйте обслуживание и проверяйте сеть с заполненным назначением и отключённым потребителем."]),
            ("gases", "mekanism:electrolytic_separator", "Gas Production and Dumping", "Производство и сброс газов",
             ["Many chemical machines stop when either gas input is empty or an unwanted coproduct tank is full. Dumping is an operating policy, not a default fix.", "Buffer every gas, document dump modes, preserve emergency oxygen or hydrogen and stop upstream production when a valuable gas destination is full."],
             ["Химические машины останавливаются при пустом входе или полном баке побочного газа. Сброс является политикой эксплуатации, а не стандартным исправлением.", "Буферизуйте газы, документируйте режимы, сохраняйте аварийный кислород или водород и останавливайте верхнюю линию при заполнении ценного назначения."]),
            ("ore2", "mekanism:enrichment_chamber", "Twofold Ore Processing", "Двойная переработка руды",
             ["Enrichment and smelting provide a compact twofold route suitable for moderate throughput and early automation.", "Measure raw input, enriched output and final ingots over one stack; use the result as a baseline before accepting the infrastructure cost of chemical multiplication."],
             ["Обогащение и плавка создают компактную двойную цепочку для умеренного выпуска и ранней автоматизации.", "Измерьте сырьё, обогащённый выход и слитки на стаке; используйте результат как базу до принятия стоимости химического умножения."]),
            ("ore3", "mekanism:purification_chamber", "Threefold Ore Processing", "Тройная переработка руды",
             ["Purification adds oxygen and clumps before crushing and enrichment. The yield matters only if the gas and downstream machines keep pace.", "Buffer oxygen and clumps, stop raw input on saturation and record the slowest stage across a complete raw-ore batch."],
             ["Очистка добавляет кислород и комки до дробления и обогащения. Выход имеет смысл только при достаточной скорости газа и нижних машин.", "Буферизуйте кислород и комки, останавливайте сырьё при заполнении и отмечайте самый медленный этап полной партии."]),
            ("ore4", "mekanism:chemical_injection_chamber", "Fourfold Ore Processing", "Четверная переработка руды",
             ["Chemical injection adds hydrogen chloride and shards. Acid precursor production, gas capacity and intermediate storage become part of the ore cost.", "Calculate net resource and energy demand, isolate shards by material and ensure acid failure stops ore delivery before partial intermediates accumulate."],
             ["Химическая инъекция добавляет хлороводород и осколки. Производство прекурсоров, газовые ёмкости и промежуточное хранение входят в стоимость руды.", "Рассчитайте ресурсы и энергию, разделите осколки и останавливайте руду при отказе кислоты до накопления незавершённых материалов."]),
            ("ore5", "mekanism:chemical_dissolution_chamber", "Fivefold Slurry Processing", "Пятерная переработка суспензии",
             ["Dissolution, washing and crystallization form a sulfuric-acid and slurry chain with multiple hazardous buffers.", "Separate dirty and clean slurry, prohibit silent chemical dumping, interlock acid input with washer and crystallizer capacity and validate the whole route with a bounded batch."],
             ["Растворение, мойка и кристаллизация образуют цепочку серной кислоты и суспензии с несколькими опасными буферами.", "Разделяйте грязную и чистую суспензию, запрещайте скрытый сброс, связывайте подачу кислоты с мощностью мойки и кристаллизатора и проверяйте ограниченной партией."]),
            ("fission", "mekanismgenerators:fission_reactor_casing", "Fission, Coolant and Waste", "Деление, охлаждение и отходы",
             ["Fission output is limited by coolant delivery, heat removal and radioactive waste handling. Raising burn rate before those systems are proven creates a delayed failure.", "Start at low burn, measure steady temperatures, buffer coolant and waste, provide shutdown logic and keep recovery equipment outside the radiation area."],
             ["Мощность деления ограничена охлаждением, отводом тепла и радиоактивными отходами. Повышение скорости до проверки систем создаёт отложенную аварию.", "Начинайте с малого горения, измеряйте температуру, буферизуйте охлаждение и отходы, создайте остановку и храните аварийное оборудование вне зоны радиации."]),
            ("fusion", "mekanismgenerators:fusion_reactor_controller", "Fusion Fuel Infrastructure", "Топливная инфраструктура синтеза",
             ["Fusion requires sustained deuterium, tritium and supporting thermal systems. A successful ignition does not prove continuous operation.", "Maintain independent fuel reserves, measure production against injection rate, plan restart energy and ensure one upstream slowdown cannot empty both fuels simultaneously."],
             ["Синтез требует устойчивого дейтерия, трития и тепловых систем. Успешный запуск не доказывает непрерывную работу.", "Храните независимые резервы, сравнивайте производство со скоростью инъекции, планируйте энергию перезапуска и не допускайте одновременного исчерпания обоих топлив."]),
            ("sps", "mekanism:sps_casing", "SPS and Antimatter", "SPS и антиматерия",
             ["The SPS converts polonium using an enormous energy budget. Antimatter is therefore a factory-capacity proof, not a passive timer.", "Provide isolated energy storage, stable polonium supply, visible progress and a shutdown threshold that protects the wider grid from complete discharge."],
             ["SPS преобразует полоний с огромным энергопотреблением. Антиматерия является доказательством мощности фабрики, а не пассивным таймером.", "Создайте изолированное хранилище энергии, стабильный полоний, видимый прогресс и порог остановки, защищающий общую сеть от полного разряда."]),
            ("project", "kubejs:antimatter_regulator", "Project: Interlocked Chemical Complex", "Проект: взаимоблокированный химический комплекс",
             ["Build a complex that sustains gases, runs at least a threefold ore chain and supports one hazardous late chemical process with automatic shutdown conditions.", "The project passes after two bounded batches, no silent dumping, visible buffer levels, documented energy draw and recovery from a deliberately blocked downstream machine."],
             ["Постройте комплекс, поддерживающий газы, минимум тройную рудную цепочку и один опасный поздний процесс с автоматическими условиями остановки.", "Проект принят после двух ограниченных партий без скрытого сброса, с видимыми уровнями, учётом энергии и восстановлением после намеренно заблокированной нижней машины."]),
        ],
    },
]


def stable_id(namespace: str) -> str:
    return hashlib.sha256(namespace.encode("utf-8")).hexdigest()[:16].upper()


def format_array(values: list[str]) -> str:
    return "[" + ",".join(json.dumps(value, ensure_ascii=False) for value in values) + "]"


def upsert(text: str, key: str, value: str) -> str:
    rendered = f"\t{key}: {value}\n"
    pattern = re.compile(rf"(?ms)^\t{re.escape(key)}:.*?(?=^\t[A-Za-z0-9_.-]+:|^\}}\s*$)")
    updated, count = pattern.subn(rendered, text, count=1)
    if count:
        return updated
    closing = text.rfind("}")
    if closing < 0:
        raise RuntimeError("Localization file has no closing brace")
    return text[:closing].rstrip() + "\n" + rendered + "}\n"


def render_chapter() -> tuple[str, str, dict[str, dict[str, str]]]:
    chapter_id = stable_id("chapter:core_technology_manual_1")
    quest_blocks: list[str] = []
    localization: dict[str, dict[str, str]] = {"en_us": {}, "ru_ru": {}}
    localization["en_us"][f"chapter.{chapter_id}.title"] = json.dumps("Core Technology Manual I", ensure_ascii=False)
    localization["ru_ru"][f"chapter.{chapter_id}.title"] = json.dumps("Основной технический справочник I", ensure_ascii=False)

    for module_index, module in enumerate(MODULES):
        previous_id = ""
        for lesson_index, lesson in enumerate(module["lessons"]):
            slug, icon, title_en, title_ru, desc_en, desc_ru = lesson
            quest_id = stable_id(f"core_manual:{module['slug']}:{slug}")
            task_id = stable_id(f"core_manual_task:{module['slug']}:{slug}")
            dependencies = f"\n\t\t\tdependencies: [\"{previous_id}\"]" if previous_id else ""
            block = (
                "\t\t{" + dependencies + "\n"
                f"\t\t\ticon: {{ id: \"{icon}\" }}\n"
                f"\t\t\tid: \"{quest_id}\"\n"
                "\t\t\tshape: \"hexagon\"\n"
                "\t\t\ttasks: [{\n"
                f"\t\t\t\tid: \"{task_id}\"\n"
                "\t\t\t\ttype: \"checkmark\"\n"
                "\t\t\t}]\n"
                f"\t\t\tx: {module_index * 8.0:.1f}d\n"
                f"\t\t\ty: {lesson_index * 2.0:.1f}d\n"
                "\t\t}"
            )
            quest_blocks.append(block)
            localization["en_us"][f"quest.{quest_id}.title"] = json.dumps(title_en, ensure_ascii=False)
            localization["en_us"][f"quest.{quest_id}.quest_desc"] = format_array(desc_en)
            localization["ru_ru"][f"quest.{quest_id}.title"] = json.dumps(title_ru, ensure_ascii=False)
            localization["ru_ru"][f"quest.{quest_id}.quest_desc"] = format_array(desc_ru)
            previous_id = quest_id

    chapter = (
        "{\n"
        "\tdefault_hide_dependency_lines: false\n"
        "\tdefault_quest_shape: \"hexagon\"\n"
        "\tfilename: \"core_technology_manual_1\"\n"
        "\tgroup: \"177A10C99EDDA376\"\n"
        "\ticon: { id: \"kubejs:mechanical_core\" }\n"
        f"\tid: \"{chapter_id}\"\n"
        "\torder_index: 4\n"
        "\tprogression_mode: \"flexible\"\n"
        "\tquest_links: []\n"
        "\tquests: [\n"
        + "\n".join(quest_blocks)
        + "\n\t]\n}\n"
    )
    return chapter_id, chapter, localization


def main() -> int:
    chapter_id, chapter, localization = render_chapter()
    previous = CHAPTER_PATH.read_text(encoding="utf-8") if CHAPTER_PATH.exists() else ""
    if previous != chapter:
        CHAPTER_PATH.write_text(chapter, encoding="utf-8", newline="\n")
        print("Core Technology Manual I chapter updated")
    else:
        print("Core Technology Manual I chapter unchanged")

    for locale, entries in localization.items():
        path = LANG_DIR / f"{locale}.snbt"
        text = path.read_text(encoding="utf-8")
        for key, value in entries.items():
            text = upsert(text, key, value)
        path.write_text(text, encoding="utf-8", newline="\n")
        print(f"{locale}: synchronized {len(entries)} manual localization entries")

    quest_total = sum(len(module["lessons"]) for module in MODULES)
    print(f"Core Technology Manual I quests: {quest_total}")
    print(f"Chapter ID: {chapter_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
