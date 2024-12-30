from enums.ime_transition import IMETransition


def di(cpu_obj):
    '''
        Requests to disable interrupts, interrupts are not disabled until the next instruction completes.
    
    '''
    cpu_obj.ime_transition = IMETransition.REQUEST_TO_OFF

def ei(cpu_obj):
    '''
        Requests to enable interrupts, interrupts are not enabled until the next instruction completes:
    '''
    cpu_obj.ime_transition = IMETransition.REQUEST_TO_ON