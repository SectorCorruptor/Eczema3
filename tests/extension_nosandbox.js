/*(function(Scratch) {
  'use strict';
  if (!Scratch.extensions.unsandboxed) {
    throw new Error();
  }
  class libsb3check {
    getInfo() {
      return {
        id: 'blahblah',
        name: 'unsandboxtest',
        blocks: [
          {
            opcode: 'test',
            blockType: Scratch.BlockType.REPORTER,
            text: 'test'
          }
        ]
      };
    }
  }
  Scratch.extensions.register(new libsb3check());
})(Scratch);*/

(function(Scratch) {
  'use strict';

  if (!Scratch.extensions.unsandboxed) {
    throw new Error('This example must run unsandboxed');
  }

  class When {
    getInfo() {
      return {
        id: 'whenunsandboxed',
        name: 'When',
        blocks: [
          {
            blockType: Scratch.BlockType.HAT,
            opcode: 'when',
            text: 'when [CONDITION]',
            isEdgeActivated: false, // required boilerplate
            arguments: {
              CONDITION: {
                type: Scratch.BlockType.BOOLEAN
              }
            }
          }
        ]
      };
    }
    when(args) {
      return Scratch.Cast.toBoolean(args.CONDITION);
    }
  }

  Scratch.vm.runtime.on('BEFORE_EXECUTE', () => {
    // startHats is the same as before!
    Scratch.vm.runtime.startHats('whenunsandboxed_when');
  });

  Scratch.extensions.register(new When());
})(Scratch);