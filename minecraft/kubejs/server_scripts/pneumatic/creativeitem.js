ServerEvents.recipes(event => {

    event.shaped(
            Item.of('pneumaticcraft:creative_compressed_iron_block'),
            [
                    'ABA',
                    'ACA',
                    'AAA'
            ],
            {
                    C: 'fragmentumneoforge:ultimatecapacitor',
                    A: 'allthecompressed:compressed_iron_block_5x',
                    B: 'pneumaticcraft:electrostatic_compressor'
            }
    )
    event.shaped(
            Item.of('pneumaticcraft:creative_compressor'),
            [
                    'ABA',
                    'ACA',
                    'AAA'
            ],
            {
                    B: 'pneumaticcraft:flux_compressor',
                    C: 'fragmentumneoforge:ultimatecapacitor',
                    A: 'allthecompressed:compressed_iron_block_5x'
            }
    )
});
