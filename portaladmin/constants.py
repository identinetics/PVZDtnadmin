STATUS_CREATED = 'created'
STATUS_UPLOADED = 'uploaded'
STATUS_REQUEST_QUEUE = 'request_queue'
STATUS_REJECTED = 'rejected'
STATUS_ACCEPTED = 'accepted'
STATUS_CHOICES = ((STATUS_CREATED, 'erstellt'),
                  (STATUS_UPLOADED, 'hochgeladen'),
                  (STATUS_REQUEST_QUEUE, 'signiert und eingebracht'),
                  (STATUS_REJECTED, 'fehlerhaft'),
                  (STATUS_ACCEPTED, 'akzeptiert'),
                  )

PUB_STATUS_PUBLISHED = 'published'
PUB_STATUS_UNPUBLISHED = 'unpublished'
PUB_STATUS_CHOICES = ((PUB_STATUS_PUBLISHED, 'veröffentlicht'),
                      (PUB_STATUS_UNPUBLISHED, 'zurückgezogen'),
                     )

