STATUS_UPLOADED = 'uploaded'
STATUS_REQUEST_QUEUE = 'request_queue'
STATUS_REJECTED = 'rejected'
STATUS_PUBLISHED = 'published'
STATUS_DELETED = 'deleted'
STATUS_CHOICES = ((STATUS_REQUEST_QUEUE, 'signiert und eingebracht'),
                  (STATUS_REJECTED, 'fehlerhaft'),
                  (STATUS_PUBLISHED, 'veröffentlicht'),
                  (STATUS_DELETED, 'gelöscht'),
                  )
