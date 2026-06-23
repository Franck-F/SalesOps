
# ===================== AUDIENCE WEB =====================
elif tab == "Audience web":
    ak = D.audience_kpis(fd)
    ad = D.audience_device(fd)
    pt = D.pages_top(fd)
    
    def fmts(secs):
        if secs < 60: return f"{int(secs)} s"
        m = int(secs) // 60
        s = int(secs) % 60
        return f"{m} min {s:02d} s"

    html = f"""
    <section style="display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:13px;margin-bottom:18px">
        <div style="background:#FFFDF8;border:1px solid color-mix(in srgb,#737D74 25%,transparent);border-radius:4px;padding:18px">
            <div style="font-size:10.5px;letter-spacing:0.08em;text-transform:uppercase;color:#737D74;font-weight:500">Sessions</div>
            <div style="font-size:25px;font-weight:700;letter-spacing:-0.02em;color:#2A432E;margin-top:10px;line-height:1;white-space:nowrap">{nb(ak['sessions'])}</div>
            <div style="font-size:11.5px;color:#737D74;margin-top:8px">sur la période</div>
        </div>
        <div style="background:#FFFDF8;border:1px solid color-mix(in srgb,#737D74 25%,transparent);border-radius:4px;padding:18px">
            <div style="font-size:10.5px;letter-spacing:0.08em;text-transform:uppercase;color:#737D74;font-weight:500">Utilisateurs</div>
            <div style="font-size:25px;font-weight:700;letter-spacing:-0.02em;color:#2A432E;margin-top:10px;line-height:1;white-space:nowrap">{nb(ak['users'])}</div>
            <div style="font-size:11.5px;color:#737D74;margin-top:8px">visiteurs uniques</div>
        </div>
        <div style="background:#FFFDF8;border:1px solid color-mix(in srgb,#737D74 25%,transparent);border-radius:4px;padding:18px">
            <div style="font-size:10.5px;letter-spacing:0.08em;text-transform:uppercase;color:#737D74;font-weight:500">Pages vues</div>
            <div style="font-size:25px;font-weight:700;letter-spacing:-0.02em;color:#2A432E;margin-top:10px;line-height:1;white-space:nowrap">{nb(int(ak['views']))}</div>
            <div style="font-size:11.5px;color:#737D74;margin-top:8px">{ak['pages_session']:.1f} / session</div>
        </div>
        <div style="background:#FFFDF8;border:1px solid color-mix(in srgb,#737D74 25%,transparent);border-radius:4px;padding:18px">
            <div style="font-size:10.5px;letter-spacing:0.08em;text-transform:uppercase;color:#737D74;font-weight:500">Durée moy. session</div>
            <div style="font-size:25px;font-weight:700;letter-spacing:-0.02em;color:#2A432E;margin-top:10px;line-height:1;white-space:nowrap">{fmts(ak['duration_s'])}</div>
            <div style="font-size:11.5px;color:#737D74;margin-top:8px">toutes sources</div>
        </div>
        <div style="background:#FFFDF8;border:1px solid color-mix(in srgb,#737D74 25%,transparent);border-radius:4px;padding:18px">
            <div style="font-size:10.5px;letter-spacing:0.08em;text-transform:uppercase;color:#737D74;font-weight:500">Pages / session</div>
            <div style="font-size:25px;font-weight:700;letter-spacing:-0.02em;color:#2A432E;margin-top:10px;line-height:1;white-space:nowrap">{ak['pages_session']:.1f}</div>
            <div style="font-size:11.5px;color:#737D74;margin-top:8px">profondeur</div>
        </div>
        <div style="background:#FFFDF8;border:1px solid color-mix(in srgb,#737D74 25%,transparent);border-radius:4px;padding:18px">
            <div style="font-size:10.5px;letter-spacing:0.08em;text-transform:uppercase;color:#737D74;font-weight:500">Taux de rebond</div>
            <div style="font-size:25px;font-weight:700;letter-spacing:-0.02em;color:#2A432E;margin-top:10px;line-height:1;white-space:nowrap">{ak['bounce_rate']*100:.0f}<span style="font-size:16px;color:#859356"> %</span></div>
            <div style="font-size:11.5px;color:#737D74;margin-top:8px">sessions 1 page</div>
        </div>
    </section>
    
    <div style="display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.3fr);gap:18px;margin-bottom:18px">
        <div style="background:#FFFDF8;border:1px solid color-mix(in srgb,#737D74 25%,transparent);border-radius:4px;padding:24px">
            <h2 style="margin:0 0 4px;font-size:16px;font-weight:700;text-transform:uppercase;letter-spacing:-0.01em;color:#2A432E">Par appareil.</h2>
            <p style="margin:0 0 18px;font-size:12px;color:#737D74">Répartition des sessions.</p>
    """
    
    dev_colors = {"mobile": "#AACB55", "desktop": "#2A432E", "tablette": "#D6E393"}
    top_device = "mobile"
    top_pct = 0
    if not ad.empty:
        top_device = ad.iloc[0]["device"]
        top_pct = ad.iloc[0]["pct_sessions"]
        for _, r in ad.iterrows():
            d_name = r["device"]
            d_pct = r["pct_sessions"]
            d_dur = fmts(r["duree_s"])
            d_reb = r["rebond"] * 100
            color = dev_colors.get(d_name, "#D6E393")
            html += f"""
            <div style="margin-bottom:15px">
                <div style="display:flex;justify-content:space-between;font-size:13px;margin-bottom:6px">
                    <span style="font-weight:500;text-transform:capitalize">{d_name}</span>
                    <span style="color:#737D74">{d_pct:.0f} % · {d_dur} · rebond {d_reb:.0f} %</span>
                </div>
                <div style="height:22px;border-radius:3px;background:color-mix(in srgb,#737D74 8%,transparent)">
                    <div style="height:100%;width:{d_pct:.1f}%;border-radius:3px;background:{color}"></div>
                </div>
            </div>
            """

    html += """
        </div>
        <div style="background:#FFFDF8;border:1px solid color-mix(in srgb,#737D74 25%,transparent);border-radius:4px;padding:24px">
            <h2 style="margin:0 0 18px;font-size:16px;font-weight:700;text-transform:uppercase;letter-spacing:-0.01em;color:#2A432E">Pages les plus vues.</h2>
            <table style="width:100%;border-collapse:collapse;font-size:13px">
                <thead>
                    <tr style="text-align:right;color:#737D74;font-size:10.5px;letter-spacing:0.06em;text-transform:uppercase">
                        <th style="text-align:left;padding:0 0 10px;font-weight:500">Page</th>
                        <th style="padding:0 0 10px;font-weight:500">Vues</th>
                        <th style="padding:0 0 10px;font-weight:500">Durée moy.</th>
                        <th style="padding:0 0 10px;font-weight:500">Sortie</th>
                    </tr>
                </thead>
                <tbody style="color:#2A432E">
    """
    
    top_conv_page = "Essai gratuit"
    if not pt.empty:
        for _, r in pt.head(8).iterrows():
            html += f"""
                    <tr style="border-top:1px solid color-mix(in srgb,#737D74 18%,transparent);text-align:right">
                        <td style="text-align:left;padding:11px 0;font-weight:500">{r['page']}</td>
                        <td style="padding:11px 0">{nb(r['vues'])}</td>
                        <td style="padding:11px 0;color:#737D74">{fmts(r['duree_s'])}</td>
                        <td style="padding:11px 0">{r['sortie']*100:.0f} %</td>
                    </tr>
            """
            
    html += f"""
                </tbody>
            </table>
        </div>
    </div>
    
    <div style="background:#FFFDF8;border:1px solid color-mix(in srgb,#737D74 25%,transparent);border-radius:4px;border-left:3px solid #AACB55;padding:18px 20px">
        <div style="font-size:13px;font-weight:600;color:#2A432E;margin-bottom:6px">Lecture</div>
        <p style="margin:0;font-size:12.5px;color:#737D74;line-height:1.5">
            <b style="color:#2A432E">{top_pct:.0f} % du trafic est {top_device}</b>. 
            L'analyse des taux de sortie par page indique les prochains chantiers d'optimisation de la conversion.
        </p>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
