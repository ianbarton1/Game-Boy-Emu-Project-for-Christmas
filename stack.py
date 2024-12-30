from number.short_int import ShortInt


def push_to_stack(cpu_obj, value:int):
    '''
        Push a value to the stack
    
    '''

    cpu_obj.stack_pointer.value -= 1
    cpu_obj.bus.write(cpu_obj.stack_pointer.value, value)

def pop_from_stack(cpu_obj)->ShortInt:
    '''
        Pop a value from the stack
    
    '''

    ret_val:ShortInt =  cpu_obj.bus.read(cpu_obj.stack_pointer.value)
    cpu_obj.stack_pointer.value += 1

    return ret_val