
rule all:
    input: 
        'completed.txt'

rule first_rule:
    output:
        'A.txt'
    shell:
        '''
        touch {output}
        '''

localrules: listener
rule listener:
    input:
        'A.txt'
    output:
        'listener_running.txt'
    shell:
        '''
        python3 listener.py script_temp job_to_bundle 3 &
        disown
        touch  {output}
        '''

rule job_to_bundle:
    input:
        infl =  'A.txt',
        lr = 'listener_running.txt'
    output:
        '{wc}.txt'
    shell:
        '''
        touch {output}
        '''

rule merge_to_one:
    input:
        expand('{wc}.txt', wc =['X', 'Y', 'Z', 'Q'])
    output:
        'completed.txt'
    shell:
        '''
        touch {output}
        '''
