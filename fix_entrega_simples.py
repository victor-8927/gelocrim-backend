conteudo = r"""import React, { useState, useEffect, useRef } from 'react';
import {
  View, Text, TouchableOpacity, StyleSheet,
  Alert, ActivityIndicator, ScrollView, Image,
  Animated, Linking
} from 'react-native';
import * as ImagePicker from 'expo-image-picker';
import * as Location from 'expo-location';

const API_URL = 'https://antsy-gloomily-query.ngrok-free.dev/api/v1';

export default function EntregaScreen({ navigation, route }) {
  const { stop, token, routeId } = route.params;
  const [foto, setFoto]       = useState(null);
  const [gps, setGps]         = useState(null);
  const [loading, setLoading] = useState(false);
  const fadeAnim              = useRef(new Animated.Value(0)).current;

  const headers = {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`,
    'ngrok-skip-browser-warning': '1'
  };

  useEffect(() => {
    obterGPS();
    Animated.timing(fadeAnim, { toValue:1, duration:500, useNativeDriver:true }).start();
  }, []);

  async function obterGPS() {
    try {
      const { status } = await Location.requestForegroundPermissionsAsync();
      if (status !== 'granted') return;
      const loc = await Location.getCurrentPositionAsync({ accuracy: Location.Accuracy.High });
      setGps(loc.coords);
    } catch {}
  }

  async function tirarFoto() {
    const { status } = await ImagePicker.requestCameraPermissionsAsync();
    if (status !== 'granted') { Alert.alert('Permissão negada', 'Câmera necessária.'); return; }
    const result = await ImagePicker.launchCameraAsync({
      mediaTypes: 'images',
      quality: 0.4,
      base64: true
    });
    if (!result.canceled) setFoto(result.assets[0]);
  }

  function abrirNavegacao() {
    const url = `https://www.google.com/maps/dir/?api=1&destination=${stop.lat},${stop.lng}&travelmode=driving`;
    Linking.openURL(url);
  }

  async function confirmarEntrega() {
    if (!foto) { Alert.alert('Atenção', 'Tire uma foto do canhoto antes de confirmar!'); return; }
    setLoading(true);
    try {
      const fotoData = foto.base64 ? `data:image/jpeg;base64,${foto.base64}` : null;
      const res = await fetch(`${API_URL}/routes/${routeId}/stops/${stop.stop_id}`, {
        method: 'PATCH',
        headers,
        body: JSON.stringify({
          status: 'completed',
          ata: new Date().toISOString(),
          lat_confirmacao: gps?.latitude,
          lng_confirmacao: gps?.longitude,
          foto_base64: fotoData,
        }),
      });
      if (res.ok) {
        Alert.alert('✅ Entrega Confirmada!', `${stop.recipient_name} registrado!`, [
          { text: 'OK', onPress: () => navigation.goBack() }
        ]);
      } else {
        Alert.alert('Erro', 'Falha ao confirmar entrega.');
      }
    } catch (e) {
      Alert.alert('Erro de Conexão', e.message);
    } finally {
      setLoading(false);
    }
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
      if (res.ok) Alert.alert('❌ Falha Registrada', motivo, [{ text: 'OK', onPress: () => navigation.goBack() }]);
    } catch (e) { Alert.alert('Erro', e.message); }
    finally { setLoading(false); }
  }

  return (
    <Animated.ScrollView style={[styles.container, { opacity: fadeAnim }]} contentContainerStyle={styles.content}>
      <View style={styles.clienteCard}>
        <Text style={styles.clienteLabel}>PRÓXIMA PARADA</Text>
        <Text style={styles.clienteSeq}>Parada {(stop.sequence||0)+1}</Text>
        <Text style={styles.clienteNome}>{stop.recipient_name}</Text>
        <Text style={styles.clienteEndereco}>{stop.address}</Text>
        <View style={styles.clienteMeta}>
          <View style={styles.metaBadge}><Text style={styles.metaBadgeTxt}>🕐 {stop.eta||'--:--'}</Text></View>
          <View style={styles.metaBadge}><Text style={styles.metaBadgeTxt}>⚖️ {(stop.weight_kg||0).toFixed(0)} kg</Text></View>
        </View>
      </View>

      <View style={styles.gpsCard}>
        <Text style={styles.gpsIcon}>📍</Text>
        {gps
          ? <Text style={styles.gpsTxt}>{gps.latitude.toFixed(5)}, {gps.longitude.toFixed(5)}</Text>
          : <Text style={styles.gpsErr}>GPS não disponível</Text>
        }
      </View>

      <TouchableOpacity style={styles.btnNav} onPress={abrirNavegacao}>
        <Text style={styles.btnNavTxt}>ABRIR NO GPS →</Text>
      </TouchableOpacity>

      <View style={styles.fotoCard}>
        <Text style={styles.fotoTitle}>FOTO DO CANHOTO</Text>
        {foto ? (
          <View>
            <Image source={{ uri: foto.uri }} style={styles.fotoPreview} />
            <TouchableOpacity style={styles.btnRetake} onPress={tirarFoto}>
              <Text style={styles.btnRetakeTxt}>📷  Tirar outra foto</Text>
            </TouchableOpacity>
          </View>
        ) : (
          <TouchableOpacity style={styles.btnFoto} onPress={tirarFoto}>
            <Text style={styles.btnFotoEmoji}>📷</Text>
            <Text style={styles.btnFotoTxt}>TIRAR FOTO DO CANHOTO</Text>
            <Text style={styles.btnFotoSub}>Obrigatório para confirmar entrega</Text>
          </TouchableOpacity>
        )}
      </View>

      <TouchableOpacity
        style={[styles.btnConfirmar, loading && { opacity: 0.6 }]}
        onPress={confirmarEntrega}
        disabled={loading}
      >
        {loading
          ? <ActivityIndicator color="#002855" />
          : <Text style={styles.btnConfirmarTxt}>❄ CONFIRMAR ENTREGA</Text>
        }
      </TouchableOpacity>

      <TouchableOpacity style={styles.btnFalha} onPress={registrarFalha} disabled={loading}>
        <Text style={styles.btnFalhaTxt}>✕  REGISTRAR FALHA</Text>
      </TouchableOpacity>
    </Animated.ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex:1, backgroundColor:'#001833' },
  content: { padding:16, gap:12, paddingBottom:32 },
  clienteCard: { backgroundColor:'rgba(0,40,85,0.95)', borderRadius:18, padding:18, borderWidth:1, borderColor:'rgba(100,180,255,0.2)' },
  clienteLabel: { color:'#64B4FF', fontSize:9, fontWeight:'800', letterSpacing:4, marginBottom:6 },
  clienteSeq: { color:'rgba(100,180,255,0.6)', fontSize:11, fontWeight:'600', marginBottom:4 },
  clienteNome: { color:'#FFFFFF', fontSize:20, fontWeight:'900', marginBottom:4 },
  clienteEndereco: { color:'rgba(255,255,255,0.45)', fontSize:12, marginBottom:12 },
  clienteMeta: { flexDirection:'row', gap:8 },
  metaBadge: { backgroundColor:'rgba(100,180,255,0.1)', borderRadius:8, paddingHorizontal:12, paddingVertical:6, borderWidth:1, borderColor:'rgba(100,180,255,0.2)' },
  metaBadgeTxt: { color:'rgba(255,255,255,0.7)', fontSize:12 },
  gpsCard: { backgroundColor:'rgba(0,200,150,0.08)', borderRadius:10, padding:12, flexDirection:'row', alignItems:'center', gap:8, borderWidth:1, borderColor:'rgba(0,200,150,0.2)' },
  gpsIcon: { fontSize:16 },
  gpsTxt: { color:'#00C896', fontSize:12, fontWeight:'600' },
  gpsErr: { color:'#FF4444', fontSize:12 },
  btnNav: { backgroundColor:'rgba(100,180,255,0.15)', borderRadius:12, padding:14, alignItems:'center', borderWidth:1, borderColor:'rgba(100,180,255,0.3)' },
  btnNavTxt: { color:'#64B4FF', fontWeight:'800', fontSize:13, letterSpacing:2 },
  fotoCard: { backgroundColor:'rgba(0,40,85,0.95)', borderRadius:16, padding:16, borderWidth:1, borderColor:'rgba(100,180,255,0.15)' },
  fotoTitle: { color:'#64B4FF', fontSize:10, fontWeight:'800', letterSpacing:3, marginBottom:12 },
  btnFoto: { borderWidth:1.5, borderColor:'rgba(100,180,255,0.3)', borderStyle:'dashed', borderRadius:12, padding:28, alignItems:'center' },
  btnFotoEmoji: { fontSize:36, marginBottom:8 },
  btnFotoTxt: { color:'#64B4FF', fontWeight:'800', fontSize:13, letterSpacing:2 },
  btnFotoSub: { color:'rgba(255,255,255,0.3)', fontSize:11, marginTop:4 },
  fotoPreview: { width:'100%', height:200, borderRadius:10 },
  btnRetake: { padding:12, alignItems:'center' },
  btnRetakeTxt: { color:'#64B4FF', fontSize:13, fontWeight:'600' },
  btnConfirmar: { backgroundColor:'#64B4FF', borderRadius:14, padding:17, alignItems:'center' },
  btnConfirmarTxt: { color:'#002855', fontWeight:'900', fontSize:15, letterSpacing:3 },
  btnFalha: { backgroundColor:'transparent', borderRadius:12, padding:14, alignItems:'center', borderWidth:1.5, borderColor:'rgba(255,68,68,0.4)', marginBottom:8 },
  btnFalhaTxt: { color:'rgba(255,100,100,0.8)', fontWeight:'700', fontSize:13, letterSpacing:2 },
});
"""

with open(r'C:\gelocrim-motorista\screens\EntregaScreen.js', 'w', encoding='utf-8') as f:
    f.write(conteudo)
print('EntregaScreen.js atualizado!')
