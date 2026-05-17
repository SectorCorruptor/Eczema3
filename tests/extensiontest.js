class libsb3check { 
    getInfo() { 
        return { 
            id: 'test', 
            name: 'test', 
            blocks: [ 
                { 
                    opcode: 'test', 
                    blockType: Scratch.BlockType.REPORTER, 
                    text: 'test' } 
                ] 
            }; 
        } 
} 
Scratch.extensions.register(new libsb3check());