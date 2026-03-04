import { useEffect, useState } from "react";
import {
  createComments,
  updateComment,
  deleteComment,
  createGeneralComment,
} from "../../utilities";


import { fetchEvent } from "../../utilities";
import { fetchComments, fetchGeneralComments } from "../../utilities";
export function useEventComments(eventId, year) {
  const [comments, setComments] = useState([]);

  // ======================
  // Tree helpers
  // ======================
  const addReply = (comments, parentId, reply) =>
    comments.map((c) =>
      c.id === parentId
        ? { ...c, replies: [...(c.replies || []), reply] }
        : { ...c, replies: addReply(c.replies || [], parentId, reply) }
    );

  const updateRecursive = (comments, updated) =>
    comments.map((c) =>
      c.id === updated.id
        ? { ...c, ...updated }
        : { ...c, replies: updateRecursive(c.replies || [], updated) }
    );

  const deleteRecursive = (comments, id) =>
    comments
      .filter((c) => c.id !== id)
      .map((c) => ({
        ...c,
        replies: deleteRecursive(c.replies || [], id),
      }));
  // ======================
  // Initial fetch
  // ======================
  useEffect(() => {
    // If neither eventId nor year is provided, do nothing
    if (!eventId && !year) return;

    let mounted = true;

    const fetchData = () => {
      if (eventId) {
        fetchComments((data) => {
          if (!mounted) return;
          setComments(data);
        }, eventId);
      } else if (year) {
        fetchGeneralComments((data) => {
          if (!mounted) return;
          setComments(data);
        }, year);
      }
    };

    fetchData();

    return () => {
      mounted = false;
    };
  }, [eventId, year]);

  // ======================
  // CRUD methods comments
  // ======================
  const create = async (data, fromWS = false) => {
    if (fromWS) {
      setComments((prev) => [...prev, data]);
      return;
    }
    let created;


    if (eventId) {
      created = await createComments(eventId, data);
    } else {
      created = await createGeneralComment(year, {...data, general: true});
    }
    if (created) {
      setComments((prev) => [...prev, created]);
    }
  };

  const reply = async (parentId, data, fromWS = false) => {
    if (fromWS) {
      setComments((prev) => addReply(prev, parentId, data));
      return;
    }

    let created;

    if (eventId) {
      created = await createComments(eventId, {
        ...data,
        parent: parentId,
      });
    } else {
      created = await createGeneralComment(year, {
        ...data,
        parent: parentId,
        general: true,
      });
    }

    if (created) {
      setComments((prev) => addReply(prev, parentId, created));
    }
  };

  const edit = async (updated, fromWS = false) => {
    if (fromWS) {
      setComments((prev) => updateRecursive(prev, updated));
      return;
    }

    const result = await updateComment(updated.id, { text: updated.text });
    if (result) {
      setComments((prev) => updateRecursive(prev, result));
    }
  };

  const like = async (id) => {
    const updated = await updateComment(id, { like: true });
    if (updated) {
      setComments((prev) => updateRecursive(prev, updated));
    }
  };

  const remove = async (id, fromWS = false) => {
    if (fromWS) {
      setComments((prev) => deleteRecursive(prev, id));
      return;
    }

    await deleteComment(id);
    setComments((prev) => deleteRecursive(prev, id));
  };

  return {
    comments,
    create,
    reply,
    edit,
    like,
    remove,
  };
}


export function useEvent(eventId) {
  const [event, setEvent] = useState(null);

  useEffect(() => {
    if (!eventId) return;
    fetchEvent(setEvent, eventId);
  }, [eventId]);

  return event;
}