export default async function handler(req, res) {
  res.setHeader("Cache-Control", "no-store");

  try {
    const { state, consume } = req.query;

    if (!state) {
      return res.status(400).json({ ok: false, error: "missing_state" });
    }

    const storage = await getStorage();
    if (!storage.ok) {
      return res.status(500).json(storage);
    }

    const key = `tiktok-oauth:${state}`;
    const payload = await storage.kv.get(key);

    if (!payload) {
      return res.status(404).json({ ok: false, error: "not_found" });
    }

    if (consume !== "false") {
      await storage.kv.del(key);
    }

    return res.status(200).json({
      ok: true,
      code: payload.code,
      state: payload.state,
      scopes: payload.scopes || "",
      receivedAt: payload.receivedAt || null,
    });
  } catch (error) {
    return res.status(500).json({
      ok: false,
      error: "server_error",
      message: error?.message || String(error),
      name: error?.name || null,
    });
  }
}

async function getStorage() {
  try {
    if (!process.env.KV_REST_API_URL || !process.env.KV_REST_API_TOKEN) {
      return {
        ok: false,
        error: "missing_kv_env",
        has_KV_REST_API_URL: Boolean(process.env.KV_REST_API_URL),
        has_KV_REST_API_TOKEN: Boolean(process.env.KV_REST_API_TOKEN),
      };
    }

    const { kv } = await import("@vercel/kv");
    return { ok: true, kv };
  } catch (error) {
    return {
      ok: false,
      error: "storage_import_failed",
      message: error?.message || String(error),
      name: error?.name || null,
    };
  }
}
