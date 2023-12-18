# shared_updates.py

def global_update_xyz(new_x, new_y, new_z, my_app_instance, my_home_instance):
    # Update the shared data source here

    # Update both instances
    if my_app_instance is not None:
        my_app_instance.updateLabels(new_x, new_y, new_z)

    if my_home_instance is not None:
        my_home_instance.updateLabels(new_x, new_y, new_z)
