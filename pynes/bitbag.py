# -*- coding: utf-8 -*-

class Joypad():

    def __init__(self, player_num, cart):
        assert player_num == 1 or player_num == 2
        self.num = player_num
        if player_num == 1:
            self.port = '$4016'
        else:
            self.port = '$4017'
        self.cart = cart
        self.actions = ['a', 'b', 'select', 'start', 
          'up', 'down', 'left', 'right']

    def __iter__(self):
        for action in self.actions:
            tag = action.capitalize()
            asm_code = (
                "JoyPad" + str(self.num) + tag + ":\n"
                "  LDA " + self.port + "\n"
                "  AND #%00000001\n"
                "  BEQ End" + tag +"\n"
            )
            index = 'joypad' + str(self.num) + '_' + action
            if index in self.cart._asm_chunks:
                asm_code += self.cart._asm_chunks[index]
            asm_code += "End" + tag + ":\n"
            yield asm_code

    def to_asm(self):
        return '\n'.join(self)

class BitPak:

    def __call__(self):
        return None

    def procedure(self):
        return None

    def attribute(self):
        return None

class rs(BitPak):

    def __call__(self, size):
        return None

    def attribute(self):
        return None


class wait_vblank(BitPak):

    def __call__(self):
        return '  JSR WAITVBLANK\n'

    def procedure(self):
        return ('WAITVBLANK:\n'
          '  BIT $2002\n'
          '  BPL WAITVBLANK\n'
          '  RTS\n')

class import_chr(BitPak):

    def __call__(self, filename):
      return ""

    def procedure(self):
      return ""

class define_sprite(BitPak):
    pass
    #(y, tile, $03, x)
    #sprite:
    #.db $80, $00, $03, $80; Y pos, tile id, attributes, X pos

class get_sprite(BitPak):

    def __call__(self):
      return None

    def procedure(self):
      return None


class load_palette(BitPak):

    def  __call__(self, palette):
        return (
          'LoadPalettes:\n'
          '  LDA $2002             ; Reset PPU, start writing\n'
          '  LDA #$3F\n'
          '  STA $2006             ; High byte = $3F00\n'
          '  LDA #$00\n'
          '  STA $2006             ; Low byte = $3F00\n'
          '  LDX #$00\n'
          'LoadPalettesIntoPPU:\n'
          '  LDA palette, x\n'
          '  STA $2007\n'
          '  INX\n'
          '  CPX #$20                  ; Hex 20 = 32 decimal\n'
          '  BNE LoadPalettesIntoPPU\n'
        )

    def procedure(self):
        return None