VDS_r (costs_r) 0 prop IQR.csv датасет основанный на VDS_r, включающий следующие индикаторы: 'ITcosts_r', 'skvozcosts_r', 'trainingcosts_r' (343 примера, мёрдж через 'okato'/'year')

VDS_r (costs_r) 1 prop IQR.csv датасет основанный на VDS_r, включающий все финансовые индикаторы: 'ITcosts_r', 'skvozcosts_r', 'trainingcosts_r', 'RDcosts_r', 'RDsalary_r', 'RDequip_r' (280 примера, мёрдж через 'okato'/'year')

VDS_r (usage_r) 0 IQR.csv датасет основанный на VDS_r, включающий следующие индикаторы 'ITusage_s', 'AIusage_s', 'BDusage_s' (322 примера, мёрдж через 'region'/'year')

VDS_r (usage_r) 0 prop IQR.csv датасет основанный на VDS_r, включающий следующие индикаторы 'ITusage_s', 'AIusage_s', 'BDusage_s' (329 примера, мёрдж через 'region'/'year')

factoriescap_r (costs_r) 0 prop IQR.csv - датасет основанный на factoriescap_r, включающий следующие индикаторы: 'ITcosts_s', 'skvozcosts_s', 'trainingcosts_s' (344 пример, мёрдж через 'region'/'year')

----


factoriescap_s (costs) 0.csv - датасет основанный на factoriescap_s, включающий следующие индикаторы: 'ITcosts_s', 'skvozcosts_s', 'trainingcosts_s' (231 пример, мёрдж через 'sector'/'year')

factoriescap_s (usage) 0.csv - датасет основанный на factoriescap_s, включающий следующие индикаторы: 'ITusage_s', 'AIusage_s', 'BDusage_s' (350 пример, мёрдж через 'sector'/'year')

factoriescap_s (research) 0 visnorm.csv - датасет основанный на factoriescap_s, включающий следующие индикаторы: 'researchorg_s', 'researchersavg_s' (330 пример, мёрдж через 'sector'/'year')

----


*Приставка prop означает, что все признаки (либо часть) представлены в форме долей, а не абсолютных величин

*Приставка visnorm предполагает визуальную нормализацию (удаление наиболее сильных выбросов)

*Приставка IQR предполагает нормализацию через межквартильный размах (удаление наиболее сильных выбросов)

*fornorm содержит величины, использованные для нормализации в диапазон от 0 до 1 (умножение на них возвращает исходный вид).
