# fix_app_motorista.py
# 1. Adiciona endpoint PATCH /routes/{route_id}/stops/{stop_id} na API
# 2. Corrige EntregaScreen.js

import os

# ── 1. ADICIONA ENDPOINT NA API ────────────────────────────────────
routes_path = r'C:\fleet-cloud\app\routers\routes.py'
with open(routes_path, 'r', encoding='utf-8') as f:
    content = f.read()

new_endpoint = '''

@router.patch("/{route_id}/stops/{stop_id}")
def update_stop(route_id: str, stop_id: str, body: dict, db=Depends(get_db)):
    """Atualiza status de uma parada (usado pelo app do motorista)"""
    from app.db_compat import now_str
    ts = now_str()

    status = body.get("status")
    ata    = body.get("ata", ts)
    atd    = body.get("atd", ts)
    failure_reason = body.get("failure_reason")

    db.execute(text("""
        UPDATE stops SET
            status = :status,
            ata = :ata,
            atd = :atd,
            failure_reason = :fr,
            updated_at = :ts
        WHERE id = :sid AND route_id = :rid
    """), {"status": status, "ata": ata, "atd": atd,
           "fr": failure_reason, "ts": ts,
           "sid": stop_id, "rid": route_id})

    # Atualiza status do pedido
    if status == "completed":
        db.execute(text("""
            UPDATE orders SET status='delivered', updated_at=:ts
            WHERE id IN (SELECT order_id FROM stops WHERE id=:sid)
        """), {"ts": ts, "sid": stop_id})
    elif status == "failed":
        db.execute(text("""
            UPDATE orders SET status='failed', updated_at=:ts
            WHERE id IN (SELECT order_id FROM stops WHERE id=:sid)
        """), {"ts": ts, "sid": stop_id})

    db.commit()
    return {"ok": True, "stop_id": stop_id, "status": status}
'''

if '/{route_id}/stops/{stop_id}' not in content:
    content = content + new_endpoint
    with open(routes_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Endpoint PATCH /stops/{stop_id} adicionado!')
else:
    print('Endpoint ja existe!')

# ── 2. CORRIGE EntregaScreen.js ───────────────────────────────────
entrega_path = r'C:\gelocrim-motorista\screens\EntregaScreen.js'

new_entrega = '''import React, { useState, useEffect } from 'react';
import {
  View, Text, TouchableOpacity, StyleSheet,
  Alert, ActivityIndicator, ScrollView, Image, Linking
} from 'react-native';
import * as ImagePicker from 'expo-image-picker';
import * as Location from 'expo-location';

const API_URL = 'http://11.0.1.72:8000/api/v1';

export default function EntregaScreen({ navigation, route }) {
  const { stop, token, routeId } = route.params;
  const [foto, setFoto] = useState(null);
  const [gps, setGps] = useState(null);
  const [loading, setLoading] = useState(false);

  const headers = {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`,
  };

  useEffect(() => { obterGPS(); }, []);

  async function obterGPS() {
    try {
      const { status } = await Location.requestForegroundPermissionsAsync();
      if (status !== 'granted') return;
      const loc = await Location.getCurrentPositionAsync({ accuracy: Location.Accuracy.High });
      setGps(loc.coords);
    } catch (e) { console.log('GPS erro:', e); }
  }

  async function tirarFoto() {
    const { status } = await ImagePicker.requestCameraPermissionsAsync();
    if (status !== 'granted') {
      Alert.alert('Permissao negada', 'Camera necessaria para tirar foto.');
      return;
    }
    const result = await ImagePicker.launchCameraAsync({
      mediaTypes: 'images',
      quality: 0.5,
      base64: false,
    });
    if (!result.canceled) setFoto(result.assets[0]);
  }

  // Abre Google Maps com rota JA DEFINIDA (sem opcoes)
  function abrirNavegacao() {
    const lat = parseFloat(stop.lat);
    const lng = parseFloat(stop.lng);
    // Origem = deposito Gelocrim
    const origemLat = -3.093544;
    const origemLng = -60.075812;
    const url = `https://www.google.com/maps/dir/?api=1&origin=${origemLat},${origemLng}&destination=${lat},${lng}&travelmode=driving`;
    Linking.openURL(url);
  }

  async function confirmarEntrega() {
    if (!foto) {
      Alert.alert('Atencao', 'Tire uma foto do canhoto antes de confirmar!');
      return;
    }
    setLoading(true);
    try {
      const payload = {
        status: 'completed',
        ata: new Date().toISOString(),
        lat_confirmacao: gps?.latitude,
        lng_confirmacao: gps?.longitude,
      };

      const res = await fetch(`${API_URL}/routes/${routeId}/stops/${stop.stop_id}`, {
        method: 'PATCH',
        headers,
        body: JSON.stringify(payload),
      });

      if (res.ok) {
        Alert.alert('Entrega Confirmada!', `${stop.recipient_name} - registrada!`, [
          { text: 'OK', onPress: () => navigation.goBack() }
        ]);
      } else {
        const err = await res.text();
        Alert.alert('Erro', `Falha ao confirmar: ${err}`);
      }
    } catch (e) {
      Alert.alert('Erro', `Falha na comunicacao: ${e.message}`);
    } finally {
      setLoading(false);
    }
  }

  async function registrarFalha() {
    Alert.alert(
      'Registrar Falha',
      'Qual o motivo?',
      [
        { text: 'Cliente ausente', onPress: () => enviarFalha('Cliente ausente') },
        { text: 'Endereco nao encontrado', onPress: () => enviarFalha('Endereco nao encontrado') },
        { text: 'Recusou entrega', onPress: () => enviarFalha('Recusou entrega') },
        { text: 'Cancelar', style: 'cancel' },
      ]
    );
  }

  async function enviarFalha(motivo) {
    setLoading(true);
    try {
      const payload = {
        status: 'failed',
        failure_reason: motivo,
        atd: new Date().toISOString(),
      };
      const res = await fetch(`${API_URL}/routes/${routeId}/stops/${stop.stop_id}`, {
        method: 'PATCH',
        headers,
        body: JSON.stringify(payload),
      });
      if (res.ok) {
        Alert.alert('Falha Registrada', motivo, [
          { text: 'OK', onPress: () => navigation.goBack() }
        ]);
      } else {
        Alert.alert('Erro', 'Nao foi possivel registrar a falha.');
      }
    } catch (e) {
      Alert.alert('Erro', `Falha na comunicacao: ${e.message}`);
    } finally {
      setLoading(false);
    }
  }

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      {/* Info do cliente */}
      <View style={styles.clienteCard}>
        <Text style={styles.clienteSeq}>Parada {(stop.sequence || 0) + 1}</Text>
        <Text style={styles.clienteNome}>{stop.recipient_name}</Text>
        <Text style={styles.clienteEndereco}>{stop.address}</Text>
        <View style={styles.clienteMeta}>
          <Text style={styles.metaItem}>ETA: {stop.eta || '--:--'}</Text>
          <Text style={styles.metaItem}>{(stop.weight_kg || 0).toFixed(0)} kg</Text>
        </View>
      </View>

      {/* GPS */}
      <View style={styles.gpsCard}>
        {gps
          ? <Text style={styles.gpsText}>GPS: {gps.latitude.toFixed(5)}, {gps.longitude.toFixed(5)}</Text>
          : <Text style={styles.gpsError}>GPS nao disponivel</Text>
        }
      </View>

      {/* Botao navegacao - rota pre-definida */}
      <TouchableOpacity style={styles.btnNav} onPress={abrirNavegacao}>
        <Text style={styles.btnNavText}>Como Chegar (Rota Planejada)</Text>
      </TouchableOpacity>

      {/* Foto do canhoto */}
      <View style={styles.fotoSection}>
        <Text style={styles.sectionTitle}>Foto do Canhoto</Text>
        {foto ? (
          <View>
            <Image source={{ uri: foto.uri }} style={styles.fotoPreview} />
            <TouchableOpacity style={styles.btnRetake} onPress={tirarFoto}>
              <Text style={styles.btnRetakeText}>Tirar outra foto</Text>
            </TouchableOpacity>
          </View>
        ) : (
          <TouchableOpacity style={styles.btnFoto} onPress={tirarFoto}>
            <Text style={styles.btnFotoText}>Tirar Foto do Canhoto</Text>
            <Text style={styles.btnFotoSub}>Obrigatorio para confirmar entrega</Text>
          </TouchableOpacity>
        )}
      </View>

      {/* Botoes */}
      <View style={styles.acoes}>
        <TouchableOpacity
          style={[styles.btnConfirmar, loading && styles.btnDisabled]}
          onPress={confirmarEntrega}
          disabled={loading}
        >
          {loading
            ? <ActivityIndicator color="#fff" />
            : <Text style={styles.btnConfirmarText}>Confirmar Entrega</Text>
          }
        </TouchableOpacity>

        <TouchableOpacity
          style={[styles.btnFalha, loading && styles.btnDisabled]}
          onPress={registrarFalha}
          disabled={loading}
        >
          <Text style={styles.btnFalhaText}>Registrar Falha</Text>
        </TouchableOpacity>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#f0f2f5' },
  content: { padding: 16, gap: 12 },
  clienteCard: { backgroundColor: '#1a1d23', borderRadius: 12, padding: 16 },
  clienteSeq: { color: '#e8521a', fontSize: 12, fontWeight: '700', marginBottom: 4 },
  clienteNome: { color: '#fff', fontSize: 18, fontWeight: '800' },
  clienteEndereco: { color: '#aaa', fontSize: 13, marginTop: 4 },
  clienteMeta: { flexDirection: 'row', gap: 16, marginTop: 8 },
  metaItem: { color: '#ccc', fontSize: 13 },
  gpsCard: { backgroundColor: '#fff', borderRadius: 10, padding: 12, borderLeftWidth: 3, borderLeftColor: '#16a34a' },
  gpsText: { color: '#16a34a', fontSize: 12 },
  gpsError: { color: '#dc2626', fontSize: 12 },
  btnNav: { backgroundColor: '#2563eb', borderRadius: 10, padding: 14, alignItems: 'center' },
  btnNavText: { color: '#fff', fontWeight: '700', fontSize: 14 },
  fotoSection: { backgroundColor: '#fff', borderRadius: 12, padding: 16 },
  sectionTitle: { fontSize: 14, fontWeight: '700', color: '#1a1d23', marginBottom: 12 },
  btnFoto: { borderWidth: 2, borderColor: '#e8521a', borderStyle: 'dashed', borderRadius: 10, padding: 24, alignItems: 'center' },
  btnFotoText: { color: '#e8521a', fontWeight: '700', fontSize: 15 },
  btnFotoSub: { color: '#888', fontSize: 12, marginTop: 4 },
  fotoPreview: { width: '100%', height: 200, borderRadius: 10 },
  btnRetake: { marginTop: 8, padding: 10, alignItems: 'center' },
  btnRetakeText: { color: '#e8521a', fontSize: 13 },
  acoes: { gap: 10, marginBottom: 24 },
  btnConfirmar: { backgroundColor: '#16a34a', borderRadius: 12, padding: 16, alignItems: 'center' },
  btnConfirmarText: { color: '#fff', fontWeight: '800', fontSize: 16 },
  btnFalha: { backgroundColor: '#fff', borderRadius: 12, padding: 16, alignItems: 'center', borderWidth: 2, borderColor: '#dc2626' },
  btnFalhaText: { color: '#dc2626', fontWeight: '700', fontSize: 15 },
  btnDisabled: { opacity: 0.6 },
});
'''

with open(entrega_path, 'w', encoding='utf-8') as f:
    f.write(new_entrega)
print('EntregaScreen.js corrigido!')
print('\nReinicie a API e pressione r no Expo!')
