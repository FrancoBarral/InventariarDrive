from ..databaseUtils.database import log_public_file
from ..email_service.email_service import send_email


def dataProcessingFilesAll(service):
    '''
    
    Receives all file data from only the files that are on my drive
    
    '''
    results = (
        service.files()
        .list(pageSize=1000, q="'me' in owners and 'root' in parents",fields="nextPageToken, files(id, name, owners, modifiedTime, mimeType)")
        .execute()
    )
    items = results.get("files", [])

    
    return converterData(items,service)


def converterData(items,service):
    '''
    
    We transform the data to save in the database later
    
    '''
    listas = list(map(lambda x: {"id": x['id'], "name": x['name'], "owner": x['owners'][0]['emailAddress'], "modifiedTime": x['modifiedTime'],"mimeType":x['mimeType'].split('/')[-1], "visibility": get_visibility(x['id'],service, x)}, items))

    return listas


def get_visibility(fileID,service,x):
    '''

    We check the visibility of the file, understanding if it is private or public, if it is public it is set to private and the corresponding email is sent to the user who owns the file notifying of the change.
    
    '''
    permissions = service.permissions().list(fileId=fileID).execute()
    is_public = any(p['type'] == 'anyone' for p in permissions.get('permissions', []))

    for permission in permissions.get('permissions', []):
        if permission.get('type') == 'anyone':

            if 'id' in permission:
                service.permissions().delete(fileId=fileID, permissionId=permission['id']).execute()
                send_email(
                    'File Visibility Changed',
                    x['owners'][0]['emailAddress'],
                    f'The visibility of your file "{x["name"]}" has been changed to private.'
                )
            else:
                print("Permission missing 'id':", permission)

            x['visibility'] = 'private'
            x['owners'] = x['owners'][0]['emailAddress']
            x['modifiedTime'] = x['modifiedTime'][:10]
            x['mimeType'] = x['mimeType'].split('/')[-1]
            log_public_file(x)

    return 'public' if is_public == "anyone" else 'private'
