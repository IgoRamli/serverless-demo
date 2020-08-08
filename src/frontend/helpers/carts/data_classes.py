# Copyright 2018 Google LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
Data class for cart items.
"""


from dataclasses import dataclass

@dataclass
class CartItem:
    """
    Data class for items in cart.
    """
    item_id: str
    modify_time: str
    uid: str
    document_id: str = None

    @staticmethod
    def deserialize(document):
        """
        Helper function for parsing a Firestore document to a CartItem object.

        Parameters:
           document (dict): A snapshot of Firestore document.

        Output:
           A CartItem object.
        """
        return CartItem(
            document_id=document['document_id'],
            item_id=document['item_id'],
            modify_time=document['modify_time'],
            uid=document['uid']
        )
