STATUS_CREATED = 'created'
STATUS_UPLOADED = 'uploaded'
STATUS_REQUEST_QUEUE = 'request_queue'
STATUS_REJECTED = 'rejected'
STATUS_ACCEPTED = 'accepted'
STATUS_SIGNATURE_APPLIED = 'signed'
STATUS_CHOICES = (
    (STATUS_CREATED, 'erstellt'),
    (STATUS_UPLOADED, 'hochgeladen'),
    (STATUS_SIGNATURE_APPLIED, 'signiert'),
    (STATUS_REQUEST_QUEUE, 'signiert und eingebracht'),
    (STATUS_REJECTED, 'fehlerhaft'),
    (STATUS_ACCEPTED, 'akzeptiert'),
)

STATUSGROUP_FRONTEND = 'frontend'
STATUSGROUP_BACKEND = 'backend'
STATUSGROUP_CHOICES = (
    (STATUSGROUP_BACKEND, STATUSGROUP_BACKEND),
    (STATUSGROUP_FRONTEND, STATUSGROUP_FRONTEND)
)

PUB_STATUS_PUBLISHED = 'published'
PUB_STATUS_UNPUBLISHED = 'unpublished'
PUB_STATUS_CHOICES = (
    (PUB_STATUS_PUBLISHED, 'veröffentlicht'),
    (PUB_STATUS_UNPUBLISHED, 'zurückgezogen'),
)


class UnittestException(Exception):
    pass
