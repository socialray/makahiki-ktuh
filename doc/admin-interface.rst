Administrator Interface
+++++++++++++++++++++++

Creating/Editing Activities
===========================

In the admin interface, click on “Activities”. There, you can click on
the add button to create a new activity or click on an activity to edit
it. The activity form is separated into 4 parts.

Basic Information
~~~~~~~~~~~~~~~~~

The basic information section contains 5 subsections.

-  The title of the activity (i.e. “Blue Planet Foundation”).
-  The description of the activity. This field uses `Markdown`_
   formatting when it is displayed to users.
-  The number of points users are to be awarded if they complete the
   activity.
-  The expected time needed to complete the activity.
-  The publication and expiration dates of the activity. Users will only
   be able to participate in these activities between these two dates.

Event
~~~~~

Here, admins have the option to make this activity an event. An event is
something that will occur at a specific date and time. The two fields
are:

-  An “Is Event?” checkbox which, if checked, marks this as an event.
-  An event date and time. This field is only required if the checkbox
   is checked.

Confirmation Type
~~~~~~~~~~~~~~~~~

This is where admins specify how the activity should be verified. There
are three different confirmation types; text, confirmation code, and
image upload. If the confirmation type is text, then the admins can
specify questions that should be asked of a user who wants to receive
credit for the activity. If the confirmation type is code, then the
system will generate confirmation codes for the activity. Finally, if
the confirmation type is image, then the user will need to upload proof
that they have completed the activity.

The fields of this section are:

-  The confirmation type, which is either “Text”, “Confirmation Code”,
   or “Image Upload”.
-  The number of confirmation codes to generate. This should only be
   entered if the confirmation type is “Confirmation Code”. If this is a
   new activity, then this field is required for activities with the
   “Confirmation Code” confirmation type. Otherwise, a number in this
   field indicates the number of additional codes to generate. There is
   also a link to view the currently generated confirmation codes.
-  The confirmation prompt, which is presented to the user when they
   either enter a confirmation code or upload an image.

Text Prompt Questions
~~~~~~~~~~~~~~~~~~~~~

This section is only if the confirmation type in the previous section is
“text”. Here, the admin can specify the questions to ask a user. The
user will be presented with a randomly picked question from this list.
The admin also needs to specify a correct answer. This answer is not
used for verification, but it does aid other admins in verifying that
the user’s response is correct.

Verifying User Participation
============================

Once users start participating in activities, they will want to receive
credit for their participation. To approve/deny these requests, go to
the admin interface and click on “ActivityMembers”. There, you will be
able to see a list of submissions. Submissions marked as “Pending
Approval” are the ones that need to be approved. Note that you can
filter by these different approval statuses on the right side.

Clicking on an entry brings you to the activity member form. Here, there
are several fields.

-  The entry’s current approval status. Change to approved if you wish
   to award this user the points for the activity. Change to rejected if
   you feel this user’s submission is inadequate.
-  The user who submitted this entry. This should not be changed.
-  The activity the user is participating in. This should not be
   changed.
-  The question asked to the user if the activity’s confirmation prompt
   is “text”. This should not be changed.
-  The response from the user. This is the field that admins should use
   to verify responses to questions.
-  An optional comment from the admin. This field should be used if the
   admin rejects the entry and needs to provide the user with a reason
   why.
-  An optional comment from the user. This field is entered by the user
   and should not be changed.
-  The uploaded image if the approval type for the activity is “Image
   Upload”. Clicking on the link views the image. This also should not
   be changed.

Be aware that approving a user provides them with points. If you choose
to reject an approved entry, then the points will be removed from the
user and they will need to resubmit their participation.

.. _Markdown: http://daringfireball.net/projects/markdown/
