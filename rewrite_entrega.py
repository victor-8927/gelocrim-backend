entrega_screen = r"""import React, { useState, useEffect, useRef } from 'react';
import {
  View, Text, TouchableOpacity, StyleSheet,
  Alert, ActivityIndicator, ScrollView, Image,
  Animated, Linking
} from 'react-native';
import * as ImagePicker from 'expo-image-picker';
import * as Location from 'expo-location';

const API_URL = 'https://antsy-gloomily-query.ngrok-free.dev/api/v1';

const CORES = {
  completed: '#00FF88',
  failed:    '#FF3355',
  reentrega: '#FFD700',
  adiada:    '#BF5FFF',
};

export default function EntregaScreen({ navigation, route }) {
  const { stop, token, routeId, proximoStop } = route.params;
  const [fotos, setFotos]       = useState({ canhoto: null, boleto: null, outros: [] });
  const [gps, setGps]           = useState(null);
  const [loading, setLoading]   = useState(false);
  const [abaFoto, setAbaFoto]   = useState('canhoto');
  const fadeAnim = useRef(new Animated.Value(0)).current;

  const headers = {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`,
    'ngrok-skip-browser-warning': '1'
  };

  useEffect(() => {
    obterGPS();
    Animated.timing(fadeAnim, { toValue: 1, duration: 400, useNativeDriver: true }).start();
  }, []);

  async function obterGPS() {
    try {
      const { status } = await Location.requestForegroundPermissionsAsync();
      if (status !== 'granted') return;
      const loc = await Location.getCurrentPositionAsync({ accuracy: Location.Accuracy.High });
      setGps(loc.coords);
    } catch {}
  }

  async function tirarFoto(categoria) {
    const { status } = await ImagePicker.requestCameraPermissionsAsync();
    if (status !== 'granted') { Alert.alert('Permissão negada', 'Câmera necessária.'); return; }
    const result = await ImagePicker.launchCameraAsync({ mediaTypes: 'images', quality: 0.5, base64: true });
    if (!result.canceled) {
      const asset = result.assets[0];
      if (categoria === 'outros') {
        setFotos(p => ({ ...p, outros: [...p.outros, asset] }));
      } else {
        setFotos(p => ({ ...p, [categoria]: asset }));
      }
    }
  }

  function abrirNavegacao() {
    const url = `https://www.google.com/maps/dir/?api=1&destination=${stop.lat},${stop.lng}&travelmode=driving`;
    Linking.openURL(url);
  }

  function mostrarProximoDestino() {
    if (!proximoStop) return;
    Alert.alert(
      '✅ Entrega Registrada!',
      `Próximo destino:\n#${(proximoStop.sequence || 0) + 1} — ${proximoStop.recipient_name}`,
      [
        { text: '🗺️ Abrir GPS', onPress: () => {
          const url = `https://www.google.com/maps/dir/?api=1&destination=${proximoStop.lat},${proximoStop.lng}&travelmode=driving`;
          Linking.openURL(url);
          navigation.goBack();
        }},
        { text: 'Voltar à Lista', onPress: () => navigation.goBack() }
      ]
    );
  }

  async function confirmarEntrega() {
    if (!fotos.canhoto) { Alert.alert('Atenção', 'Foto do canhoto é obrigatória!'); return; }
    setLoading(true);
    try {
      const fotosCombinadas = {
        canhoto: fotos.canhoto?.base64 ? `data:image/jpeg;base64,${fotos.canhoto.base64}` : null,
        boleto:  fotos.boleto?.base64  ? `data:image/jpeg;base64,${fotos.boleto.base64}`  : null,
      };
      const res = await fetch(`${API_URL}/routes/${routeId}/stops/${stop.stop_id}`, {
        method: 'PATCH', headers,
        body: JSON.stringify({
          status: 'completed',
          ata: new Date().toISOString(),
          lat_confirmacao: gps?.latitude,
          lng_confirmacao: gps?.longitude,
          foto_base64: fotosCombinadas.canhoto,
        }),
      });
      if (res.ok) {
        mostrarProximoDestino();
      } else {
        Alert.alert('Erro', 'Falha ao confirmar entrega.');
      }
    } catch (e) { Alert.alert('Erro de Conexão', e.message); }
    finally { setLoading(false); }
  }

  async function registrarReentrega() {
    Alert.alert('Solicitar Reentrega', 'Motivo:', [
      { text: 'Cliente não estava',      onPress: () => enviarReentrega('Cliente não estava') },
      { text: 'Sem espaço no freezer',   onPress: () => enviarReentrega('Sem espaço no freezer') },
      { text: 'Horário incompatível',    onPress: () => enviarReentrega('Horário incompatível') },
      { text: 'Cancelar', style: 'cancel' },
    ]);
  }

  async function enviarReentrega(motivo) {
    setLoading(true);
    try {
      await fetch(`${API_URL}/routes/${routeId}/stops/${stop.stop_id}`, {
        method: 'PATCH', headers,
        body: JSON.stringify({ status: 'reentrega', failure_reason: motivo }),
      });
      Alert.alert('🟡 Reentrega Solicitada', 'A Torre de Controle vai analisar e notificar você.', [
        { text: 'Próximo cliente', onPress: () => navigation.goBack() }
      ]);
    } catch (e) { Alert.alert('Erro', e.message); }
    finally { setLoading(false); }
  }

  async function registrarFalha() {
    Alert.alert('Registrar Falha', 'Motivo da não entrega:', [
      { text: 'Cliente ausente',          onPress: () => enviarFalha('Cliente ausente') },
      { text: 'Endereço não encontrado',  onPress: () => enviarFalha('Endereço não encontrado') },
      { text: 'Recusou a entrega',        onPress: () => enviarFalha('Recusou a entrega') },
      { text: 'Cancelar', style: 'cancel' },
    ]);
  }

  async function enviarFalha(motivo) {
    setLoading(true);
    try {
      const res = await fetch(`${API_URL}/routes/${routeId}/stops/${stop.stop_id}`, {
        method: 'PATCH', headers,
        body: JSON.stringify({ status: 'failed', failure_reason: motivo, atd: new Date().toISOString() }),
      });
      if (res.ok) Alert.alert('🔴 Falha Registrada', motivo, [
        { text: 'OK', onPress: () => navigation.goBack() }
      ]);
    } catch (e) { Alert.alert('Erro', e.message); }
    finally { setLoading(false); }
  }

  return (
    <Animated.ScrollView style={[styles.container, { opacity: fadeAnim }]} contentContainerStyle={styles.content}>
      {/* Card cliente */}
      <View style={styles.clienteCard}>
        <View style={{ flexDirection: 'row', justifyContent: 'space-between', alignItems: 'flex-start' }}>
          <View style={{ flex: 1 }}>
            <Text style={styles.clienteLabel}>PARADA #{(stop.sequence || 0) + 1}</Text>
            <Text style={styles.clienteNome}>{stop.recipient_name}</Text>
            <Text style={styles.clienteCod}>COD SANKHYA: {stop.codparc || '—'}</Text>
            <Text style={styles.clienteEndereco}>{stop.address}</Text>
          </View>
          <TouchableOpacity style={styles.btnMaps} onPress={abrirNavegacao}>
            <Text style={{ fontSize: 20 }}>🗺️</Text>
          </TouchableOpacity>
        </View>
        <View style={styles.clienteMeta}>
          <View style={styles.metaBadge}><Text style={styles.metaBadgeTxt}>🕐 {stop.eta || '--:--'}</Text></View>
          <View style={styles.metaBadge}><Text style={styles.metaBadgeTxt}>⚖️ {(stop.weight_kg || 0).toFixed(0)} kg</Text></View>
        </View>
      </View>

      {/* GPS */}
      <View style={styles.gpsCard}>
        <Text style={{ fontSize: 14 }}>📍</Text>
        {gps
          ? <Text style={styles.gpsTxt}>{gps.latitude.toFixed(5)}, {gps.longitude.toFixed(5)}</Text>
          : <Text style={styles.gpsErr}>Aguardando GPS...</Text>
        }
      </View>

      {/* Fotos multicategoria */}
      <View style={styles.fotoCard}>
        <Text style={styles.fotoTitle}>📸 COMPROVANTES</Text>
        
        {/* Abas de categoria */}
        <View style={styles.abaRow}>
          {[['canhoto','Canhoto*'],['boleto','Boleto'],['outros','Outros']].map(([k,lb]) => (
            <TouchableOpacity key={k} style={[styles.aba, abaFoto===k && styles.abaAtiva]}
              onPress={() => setAbaFoto(k)}>
              <Text style={[styles.abaTxt, abaFoto===k && styles.abaTxtAtiva]}>
                {lb} {k==='canhoto' && fotos.canhoto ? '✅' : k==='boleto' && fotos.boleto ? '✅' : k==='outros' && fotos.outros.length > 0 ? `(${fotos.outros.length})` : ''}
              </Text>
            </TouchableOpacity>
          ))}
        </View>

        {/* Área da foto */}
        {abaFoto === 'outros' ? (
          <View>
            <View style={{ flexDirection: 'row', flexWrap: 'wrap', gap: 8 }}>
              {fotos.outros.map((f, i) => (
                <Image key={i} source={{ uri: f.uri }} style={styles.fotoThumb} />
              ))}
              <TouchableOpacity style={styles.btnAddFoto} onPress={() => tirarFoto('outros')}>
                <Text style={{ fontSize: 24, color: '#00BFFF' }}>+</Text>
              </TouchableOpacity>
            </View>
          </View>
        ) : (
          fotos[abaFoto] ? (
            <View>
              <Image source={{ uri: fotos[abaFoto].uri }} style={styles.fotoPreview} />
              <TouchableOpacity style={styles.btnRetake} onPress={() => tirarFoto(abaFoto)}>
                <Text style={styles.btnRetakeTxt}>📷 Tirar outra foto</Text>
              </TouchableOpacity>
            </View>
          ) : (
            <TouchableOpacity style={styles.btnFoto} onPress={() => tirarFoto(abaFoto)}>
              <Text style={styles.btnFotoEmoji}>📷</Text>
              <Text style={styles.btnFotoTxt}>
                {abaFoto === 'canhoto' ? 'FOTO DO CANHOTO (OBRIGATÓRIO)' :
                 abaFoto === 'boleto'  ? 'FOTO DO BOLETO (OPCIONAL)' : 'ADICIONAR FOTO'}
              </Text>
            </TouchableOpacity>
          )
        )}
      </View>

      {/* Confirmar entrega */}
      <TouchableOpacity
        style={[styles.btnConfirmar, loading && { opacity: 0.6 }]}
        onPress={confirmarEntrega} disabled={loading}>
        {loading ? <ActivityIndicator color="#001020" /> :
          <Text style={styles.btnConfirmarTxt}>✅ CONFIRMAR ENTREGA</Text>}
      </TouchableOpacity>

      {/* Reentrega */}
      <TouchableOpacity style={styles.btnReentrega} onPress={registrarReentrega} disabled={loading}>
        <Text style={styles.btnReentregaTxt}>🟡 SOLICITAR REENTREGA</Text>
      </TouchableOpacity>

      {/* Falha */}
      <TouchableOpacity style={styles.btnFalha} onPress={registrarFalha} disabled={loading}>
        <Text style={styles.btnFalhaTxt}>🔴 REGISTRAR FALHA</Text>
      </TouchableOpacity>
    </Animated.ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#001020' },
  content: { padding: 16, gap: 12, paddingBottom: 40 },
  clienteCard: { backgroundColor: 'rgba(0,30,60,0.95)', borderRadius: 16, padding: 16, borderWidth: 1, borderColor: 'rgba(0,191,255,0.3)' },
  clienteLabel: { color: '#00BFFF', fontSize: 9, fontWeight: '800', letterSpacing: 4, marginBottom: 4 },
  clienteNome: { color: '#FFFFFF', fontSize: 18, fontWeight: '900', marginBottom: 2 },
  clienteCod: { color: '#00BFFF', fontSize: 11, fontWeight: '600', marginBottom: 2 },
  clienteEndereco: { color: 'rgba(255,255,255,0.45)', fontSize: 11, marginBottom: 10 },
  clienteMeta: { flexDirection: 'row', gap: 8 },
  metaBadge: { backgroundColor: 'rgba(0,191,255,0.1)', borderRadius: 8, paddingHorizontal: 10, paddingVertical: 5, borderWidth: 1, borderColor: 'rgba(0,191,255,0.2)' },
  metaBadgeTxt: { color: 'rgba(255,255,255,0.7)', fontSize: 11 },
  btnMaps: { width: 44, height: 44, borderRadius: 22, backgroundColor: 'rgba(0,191,255,0.15)', alignItems: 'center', justifyContent: 'center', borderWidth: 1, borderColor: 'rgba(0,191,255,0.3)' },
  gpsCard: { backgroundColor: 'rgba(0,255,136,0.08)', borderRadius: 10, padding: 10, flexDirection: 'row', alignItems: 'center', gap: 8, borderWidth: 1, borderColor: 'rgba(0,255,136,0.2)' },
  gpsTxt: { color: '#00FF88', fontSize: 11, fontWeight: '600' },
  gpsErr: { color: '#FF3355', fontSize: 11 },
  fotoCard: { backgroundColor: 'rgba(0,30,60,0.95)', borderRadius: 16, padding: 16, borderWidth: 1, borderColor: 'rgba(0,191,255,0.15)' },
  fotoTitle: { color: '#00BFFF', fontSize: 10, fontWeight: '800', letterSpacing: 3, marginBottom: 12 },
  abaRow: { flexDirection: 'row', gap: 8, marginBottom: 12 },
  aba: { flex: 1, padding: 8, borderRadius: 8, backgroundColor: 'rgba(255,255,255,0.05)', borderWidth: 1, borderColor: 'rgba(255,255,255,0.1)', alignItems: 'center' },
  abaAtiva: { backgroundColor: 'rgba(0,191,255,0.2)', borderColor: '#00BFFF' },
  abaTxt: { color: 'rgba(255,255,255,0.4)', fontSize: 11, fontWeight: '600' },
  abaTxtAtiva: { color: '#00BFFF' },
  btnFoto: { borderWidth: 1.5, borderColor: 'rgba(0,191,255,0.3)', borderStyle: 'dashed', borderRadius: 12, padding: 24, alignItems: 'center' },
  btnFotoEmoji: { fontSize: 32, marginBottom: 8 },
  btnFotoTxt: { color: '#00BFFF', fontWeight: '800', fontSize: 12, letterSpacing: 1, textAlign: 'center' },
  fotoPreview: { width: '100%', height: 200, borderRadius: 10 },
  fotoThumb: { width: 80, height: 80, borderRadius: 8 },
  btnAddFoto: { width: 80, height: 80, borderRadius: 8, borderWidth: 1.5, borderColor: 'rgba(0,191,255,0.3)', borderStyle: 'dashed', alignItems: 'center', justifyContent: 'center' },
  btnRetake: { padding: 10, alignItems: 'center' },
  btnRetakeTxt: { color: '#00BFFF', fontSize: 12, fontWeight: '600' },
  btnConfirmar: { backgroundColor: '#00FF88', borderRadius: 14, padding: 16, alignItems: 'center' },
  btnConfirmarTxt: { color: '#001020', fontWeight: '900', fontSize: 14, letterSpacing: 2 },
  btnReentrega: { backgroundColor: 'transparent', borderRadius: 12, padding: 14, alignItems: 'center', borderWidth: 1.5, borderColor: '#FFD700' },
  btnReentregaTxt: { color: '#FFD700', fontWeight: '700', fontSize: 13, letterSpacing: 1 },
  btnFalha: { backgroundColor: 'transparent', borderRadius: 12, padding: 14, alignItems: 'center', borderWidth: 1.5, borderColor: 'rgba(255,51,85,0.5)', marginBottom: 8 },
  btnFalhaTxt: { color: '#FF3355', fontWeight: '700', fontSize: 13, letterSpacing: 1 },
});
"""

with open(r'C:\gelocrim-motorista\screens\EntregaScreen.js', 'w', encoding='utf-8') as f:
    f.write(entrega_screen)
print('EntregaScreen.js reescrito!')
