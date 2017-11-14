import json
from os import getcwd

from scannerpy import BulkJob, ColumnType, Database, DeviceType, Job
from scannerpy.stdlib import writers

cwd = getcwd()
with Database() as db:
    title = 'zootopia_2016'

    # Register the carnie kernel
    db.register_op('GenderDetect', [('frame', ColumnType.Video), 'bboxes'],
                   ['genders'])
    db.register_python_kernel('GenderDetect', DeviceType.CPU,
                              cwd + '/carnie_kernel.py')

    frame = db.ops.FrameInput()
    frame_strided = frame.sample()
    bboxes = db.ops.Input()
    genders = db.ops.GenderDetect(frame=frame_strided, bboxes=bboxes)
    output = db.ops.Output(columns=[genders])
    job = Job(op_args={
        frame: db.table(title).column('frame'),
        frame_strided: db.sampler.strided(24),
        bboxes: db.table(title + "_bboxes").column('bboxes'),
        output: title + '_genders',
    })

    # run job
    bulk_job = BulkJob(output=output, jobs=[job])
    db.run(bulk_job, force=True, pipeline_instances_per_node=1)
    output_tables = db.table(title).column('genders').toarray()
    gender_outputs = output_tables[0].load(['genders'])
    json.dump(gender_outputs, title + '_gender.json')
